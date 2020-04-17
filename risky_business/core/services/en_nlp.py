from spacy import load

from django.utils import timezone

from core.services.base import AbstractNlpService
from core.models.aup import Keyword
from core.models.aup import Phrase


class EnglishNLPService(AbstractNlpService):
    def __init__(self, snippet):
        super(EnglishNLPService, self).__init__(snippet)
        nlp = load("en_core_web_sm")
        self.snippet = snippet
        self.doc = nlp(snippet.text)
        self.previous_results = self.results_set.last()
        self.is_against_aup = False
        self.risk_level = 0
        self.report = {}

    def process(self):
        """
        Gather data and collect to report and save results
        """
        self.get_nlp_data()
        self.check_against_aup()
        self.add_process_time()
        self.save_results()

    def add_process_time(self):
        self.snippet.process_time = timezone.now()
        self.snippet.processed = True
        self.snippet.save()

    def to_bytes(self):
        return self.doc.to_bytes()

    def check_against_aup(self):
        """
        Check all lemmas and noun chunks against keywords and phrases.
        Map which AUP rules get hit.
        """
        hits = {}
        lemmas = self.report['data']['lemmas']
        noun_chunks = self.report['data']['noun_chunks']

        hit_keywords = Keyword.objects.filter(keyword__in=lemmas)
        for hit in hit_keywords:
            hits[hit.keyword] = [aup_rule.full_rule for aup_rule in
                                     hit.aup_rule.all()]

        phrases = Phrase.objects.all()
        for phrase in phrases:
            for chunk in noun_chunks:
                if phrase.phrase in chunk:
                    hits[phrase.phrase] = [
                    {
                        'aup': aup_rule.full_rule,
                        'message': aup_rule.hit_message,
                        'decision': aup_rule.decision,
                     }
                    for aup_rule in
                         phrase.aup_rule.all()
                ]

        if hits:
            self.is_against_aup = True
        self.report['hits'] = hits

    def assess_risk_level(self):
        pass

    def get_nlp_data(self):
        lemmas = self.get_lemmatized_words()
        is_real_sentence = self.check_if_real_sentence(lemmas=lemmas)
        noun_chunks = self.get_noun_chunks()
        ents = self.get_entities()
        data = {
            'lemmas': lemmas,
            'is_real_sentence': is_real_sentence,
            'ents': ents,
            'noun_chunks': noun_chunks
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

    def get_noun_chunks(self):
        """
        Get all found noun chunks
        """
        noun_chunks = []
        for chunk in self.doc.noun_chunks:
            noun_chunks.append(chunk.text.lower())

        return noun_chunks

    def save_results(self):
        results = self.snippet.results_set.create(
            snippet=self.snippet,
            binary_results=self.to_bytes(),
            is_against_aup=self.is_against_aup,
            assessed_risk_level=self.risk_level,
            report=self.report,
        )

        return results
