from spacy import load
from core.services.base import AbstractNlpService
from core.services.exceptions import UnknownWordsError


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
        lemmas = self.get_lemmas()
        ents = self.get_ents()

        self.report = {
            'lemmas': lemmas,
            'ents': ents,
        }
        self.save_results()

    def to_bytes(self):
        return self.doc.to_bytes()

    def check_against_aup(self):
        pass

    def assess_risk_level(self):
        pass

    def create_report(self):
        pass

    def get_lemmas(self):
        """
        get POS token data for all non stopwords and punctuation
        """
        lemmas = []
        for word in self.doc:
            if not word.is_stop and word.pos_ != 'PUNCT' and not word.like_num:
                lemmas.append(word.lemma_)
        if len(lemmas) < 1:
            raise UnknownWordsError("Text is gibberish!")
        return lemmas

    def get_ents(self):
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
