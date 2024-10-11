from abc import ABC, abstractmethod


class CommandAnalyzerService(ABC):
    @abstractmethod
    def requestToInjectReceiverAnalyzerChannel(self, ipcReceiverAnalyzerChannel):
        pass

    @abstractmethod
    def requestToInjectAnalyzerExecutorChannel(self, ipcAnalyzerExecutorChannel):
        pass

    @abstractmethod
    def analysisCommand(self, analyzerId):
        pass
