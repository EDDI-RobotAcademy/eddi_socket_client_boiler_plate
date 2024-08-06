from abc import ABC, abstractmethod


class CommandAnalyzerService(ABC):
    @abstractmethod
    def analysisCommand(self):
        pass
