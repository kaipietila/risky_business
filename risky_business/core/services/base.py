import abc


class AbstractNlpService(abc.ABC):
    def __init__(self, snippet):
        self.snippet = snippet

    @abc.abstractmethod
    def process(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def to_bytes(self):
        raise NotImplementedError()

    @property
    def results_set(self):
        return self.snippet.results_set