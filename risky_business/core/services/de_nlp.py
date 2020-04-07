from spacy import load
from core.services.base import AbstractNlpService


class GermanNLPService(AbstractNlpService):
    def __init__(self, snippet):
        super(GermanNLPService, self).__init__(snippet)
        self.nlp = load("de_core_news_sm")

    def process_snippet(self):
        pass

    def to_bytes(self):
        pass
