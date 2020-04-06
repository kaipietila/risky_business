from spacy import load
from django.conf import settings
from risky_business.core.services.base import AbstractNlpService


class GermanNLPService(AbstractNlpService):
    def __init__(self, snippet):
        super(GermanNLPService, self).__init__(snippet)
        self.nlp = load(settings.SPACY_DE_SM_PACKAGE)

    def process_snippet(self):
        pass

    def to_bytes(self):
        pass
