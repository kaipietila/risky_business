from spacy import load

from django.utils import timezone

from core.services.base import AbstractNlpService
from core.models.aup import Keyword


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
        self.get_ents()
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
        Get all keywords and check against them and map which AUP
        rules get hit, by checking against the lemmatized forms of words
        and add them to report
        """
        keywords = Keyword.objects.all()
        hits = {}
        lemmas = self.report['data']['lemmas']
        for keyword in keywords:
            if keyword.keyword in lemmas:
                hits[keyword.keyword] = [aup_rule.full_rule for aup_rule in
                                         keyword.aup_rule.all()]
        if hits:
            self.is_against_aup = True
        self.report['hits'] = hits

    def assess_risk_level(self):
        pass

    def create_report(self):
        pass

    def get_nlp_data(self):
        lemmas = self.get_lemmas()
        is_real_sentence = self.check_if_real_sent(lemmas=lemmas)
        data = {
            'lemmas': lemmas,
            'is_real_sentence': is_real_sentence,
        }
        self.report['data'] = data

    def check_if_real_sent(self, lemmas):
        """
        Checks is sentence does not contain anything else than stopwords,
        numbers or punctuation. If no lemmas is found still checks spacy
        doc.sents if it has been able to segment a sentence.
        """
        is_real_sentence = False
        if len(lemmas):
            is_real_sentence = True

        if not is_real_sentence and len(self.doc.sents) <= 1:
            is_real_sentence = True

        return is_real_sentence

    def get_lemmas(self):
        """
        get POS token data for all non stopwords and punctuation
        """
        lemmas = []
        for word in self.doc:
            if not word.is_stop and word.pos_ != 'PUNCT' and not word.like_num:
                lemmas.append(word.lemma_)
        return lemmas

    def get_ents(self):
        """
        Get all found entities
        """
        ents = {}
        for ent in self.doc.ents:
            ents[ent.text] = ent.label_

        self.report['ents'] = ents

    def save_results(self):
        results = self.snippet.results_set.create(
            snippet=self.snippet,
            binary_results=self.to_bytes(),
            is_against_aup=self.is_against_aup,
            assessed_risk_level=self.risk_level,
            report=self.report,
        )

        return results
