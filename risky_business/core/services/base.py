import abc

from risky_business.core.models.nlp import Snippet


class AbstractNlpService(abc.ABC):
    def __init__(self, snippet):
        self.snippet = Snippet.objects.get(code=snippet)

    @abc.abstractmethod
    def process_snippet(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def to_bytes(self):
        raise NotImplementedError()


