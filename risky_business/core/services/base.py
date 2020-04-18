import abc

from core.models.aup import Keyword
from core.models.aup import Phrase


class AbstractNlpService(abc.ABC):
    def __init__(self, snippet):
        self.snippet = snippet

    @staticmethod
    def get_phrases_list(language):
        phrases_list = [phrase.phrase for phrase in
                        Phrase.objects.filter(language=language)]

        return phrases_list

    @staticmethod
    def get_keywords_list(language):
        keywords_list = [keyword.keyword for keyword in
                         Keyword.objects.filter(language=language)]
        return keywords_list

    @abc.abstractmethod
    def process(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def to_bytes(self):
        raise NotImplementedError()

    @property
    def results_set(self):
        return self.snippet.results_set