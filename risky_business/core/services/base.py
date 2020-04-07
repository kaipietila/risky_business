import abc

from core.models.nlp import Snippet


class AbstractNlpService(abc.ABC):
    def __init__(self, snippet):
        self.snippet = Snippet.objects.get(code=snippet)

    @abc.abstractmethod
    def process_snippet(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def to_bytes(self):
        raise NotImplementedError()

    @property
    def results_set(self):
        return self.snippet.results_set