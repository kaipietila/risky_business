from spacy import load
from django.conf import settings
from risky_business.core.services.base import AbstractNlpService


class EnglishNLPService(AbstractNlpService):
    def __init__(self, snippet):
        super(EnglishNLPService, self).__init__(snippet)
        self.nlp = load(settings.SPACY_EN_SM_PACKAGE)

    def process_snippet(self):
        pass

    def to_bytes(self):
        pass

