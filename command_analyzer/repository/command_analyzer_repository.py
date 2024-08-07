from abc import ABC, abstractmethod


class CommandAnalyzerRepository(ABC):
    @abstractmethod
    def injectReceiverAnalyzerChannel(self, ipcReceiverAnalyzerChannel):
        pass

    @abstractmethod
    def injectAnalyzerExecutorChannel(self, ipcAnalyzerExecutorChannel):
        pass

    @abstractmethod
    def acquireNeedToAnalysisRequestedData(self):
        pass

    @abstractmethod
    def sendDataToCommandExecutor(self, willBeExecuteData):
        pass
