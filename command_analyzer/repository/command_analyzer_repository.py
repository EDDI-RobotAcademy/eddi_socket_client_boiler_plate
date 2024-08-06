from abc import ABC, abstractmethod


class CommandAnalyzerRepository(ABC):
    @abstractmethod
    def analysis(self):
        pass
