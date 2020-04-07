from spacy import load
from core.services.base import AbstractNlpService


class EnglishNLPService(AbstractNlpService):
    def __init__(self, snippet):
        super(EnglishNLPService, self).__init__(snippet)
        nlp = load("en_core_web_sm")
        self.doc = nlp(snippet.text)
        self.previous_results = self.results_set.last()

    def process_snippet(self):
        pos = self.get_pos()
        lemmas = [word['lemma'] for word in pos]
        ents = self.get_ents()

    def to_bytes(self):
        return self.doc.to_bytes()

    def check_against_aup(self):
        pass

    def get_pos(self):
        """
        get POS token data for all non stopwords and punctuation
        """
        pos = {}
        for word in self.doc:
            if not word.is_stop and word.pos_ != 'PUNCT' and word.like_num:
                pos[str(word)] = [word.lemma, word.pos_, word.dep_]
        return pos

    def get_ents(self):
        """
        Get all found entities
        """
        ents = {}
        for ent in self.doc.ents:
            ent[ent.text] = ent.label_
        return ents
