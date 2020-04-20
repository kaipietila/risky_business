from spacy import load
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

from django.utils import timezone
from django.db.models import Q

from core.services.base import AbstractNlpService
from core.models.aup import Keyword
from core.models.aup import Phrase


class EnglishNLPService(AbstractNlpService):
    def __init__(self, snippet):
        super(EnglishNLPService, self).__init__(snippet)
        self.nlp = load("en_core_web_sm")
        self.snippet = snippet
        self.is_against_aup = False
        self.report = {}
        self.risk_level = 0

        self.create_matchers(self.nlp)

        self.doc = self.nlp(snippet.text.lower())

    def create_matchers(self, nlp):
        # One matcher for phrases, one for keywords and one for
        # manually entered patterns for harder to match phrases
        self.phrase_matcher = PhraseMatcher(nlp.vocab, attr='LEMMA')
        phrase_matcher_list = self.get_phrases_list('EN')
        phrase_patterns = [(nlp(phrase[0]), phrase[1]) for phrase in phrase_matcher_list]
        for pattern, pattern_object_id in phrase_patterns:
            self.phrase_matcher.add(str(pattern_object_id), None, pattern)

        self.keyword_matcher = PhraseMatcher(nlp.vocab, attr='LEMMA')
        keyword_matcher_list = self.get_keywords_list('EN')
        keyword_patterns = [(nlp(keyword[0]), keyword[1]) for keyword in keyword_matcher_list]
        for pattern, pattern_object_id in keyword_patterns:
            self.keyword_matcher.add(str(pattern_object_id), None, pattern)

        self.pattern_matcher = Matcher(nlp.vocab)
        pattern_list = self.get_manually_entered_patterns('EN')
        for pattern, pattern_object_id in pattern_list:
            self.pattern_matcher.add(str(pattern_object_id), None, pattern)

    def process(self):
        """
        Gather data and collect to report and save results
        """
        self.get_nlp_data()
        self.check_against_aup()
        self.get_matches()
        self.add_process_time()
        self.save_results()

    def add_process_time(self):
        self.snippet.process_time = timezone.now()
        self.snippet.processed = True
        self.snippet.save()

    def to_bytes(self):
        return self.doc.to_bytes()

    def get_matches(self):
        phrase_matches = []
        keyword_matches = []
        pattern_matches = []
        hits = self.phrase_matcher(self.doc)
        for match_id, start, end in hits:
            phrase_matches.append(self.nlp.vocab.strings[match_id])
        hits = self.keyword_matcher(self.doc)
        for match_id, start, end in hits:
            keyword_matches.append(self.nlp.vocab.strings[match_id])
        hits = self.pattern_matcher(self.doc)
        for match_id, start, end in hits:
            pattern_matches.append(self.nlp.vocab.strings[match_id])
        return phrase_matches, keyword_matches, pattern_matches

    def check_against_aup(self):
        """
        Check all lemmas and noun chunks against keywords and phrases.
        Map which AUP rules get hit.
        """
        phrase_matches, keyword_matches, pattern_matches = self.get_matches()
        hits = {}

        keywords = Keyword.objects.filter(id__in=keyword_matches)
        for word in keywords:
            hits[word.keyword] = [aup_rule.full_rule for aup_rule in
                                     word.aup_rule.all()]

        phrase_query = Q(id__in=phrase_matches) | Q(id__in=pattern_matches)
        phrases = Phrase.objects.filter(phrase_query)
        for phrase in phrases:
            hits[phrase.phrase] = [aup_rule.full_rule for aup_rule in
                                     phrase.aup_rule.all()]


        if hits:
            self.is_against_aup = True
        self.report['hits'] = hits

    def get_nlp_data(self):
        """
        Currently only used to show data for debugging purposes
        """
        lemmas = self.get_lemmatized_words()
        is_real_sentence = self.check_if_real_sentence(lemmas=lemmas)
        ents = self.get_entities()
        data = {
            'lemmas': lemmas,
            'is_real_sentence': is_real_sentence,
            'ents': ents,
        }
        self.report['data'] = data

    def check_if_real_sentence(self, lemmas):
        """
        Checks is sentence does not contain anything else than stopwords,
        numbers or punctuation. If no lemmas is found still checks spacy
        doc.sents if it has been able to segment a sentence.
        """
        is_real_sentence = False
        if len(lemmas):
            is_real_sentence = True

        if not is_real_sentence and not self.doc.sents:
            is_real_sentence = True

        return is_real_sentence

    def get_lemmatized_words(self):
        """
        get POS token data for all non stopwords and punctuation
        """
        lemmas = []
        for word in self.doc:
            if not word.is_stop and not word.is_punct and not word.like_num:
                lemmas.append(word.lemma_)
        return lemmas

    def get_entities(self):
        """
        Get all found entities
        """
        ents = {}
        for ent in self.doc.ents:
            ents[ent.text] = ent.label_

        return ents

    def save_results(self):
        results = self.snippet.results_set.create(
            snippet=self.snippet,
            binary_results=self.to_bytes(),
            is_against_aup=self.is_against_aup,
            assessed_risk_level=self.risk_level,
            report=self.report,
        )

        return results
