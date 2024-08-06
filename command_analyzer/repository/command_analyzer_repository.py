from abc import ABC, abstractmethod


class CommandAnalyzerRepository(ABC):
    @abstractmethod
    def injectReceiverAnalyzerChannel(self, ipcReceiverAnalyzerChannel):
        pass

    @abstractmethod
    def injectAnalyzerExecutorChannel(self, ipcAnalyzerExecutorChannel):
        pass

    @abstractmethod
    def analysis(self):
        pass
