from spacy.lang.fi import Finnish
from core.services.base import AbstractNlpService

"""
Spacy does not support Finnish as a full model yet, so results may not be good
"""


class FinnishNLPService(AbstractNlpService):
    def __init__(self, snippet):
        super(FinnishNLPService, self).__init__(snippet)
        self.nlp = Finnish()

    def process_snippet(self):
        pass

    def to_bytes(self):
        pass

    def check_against_aup(self):
        pass
