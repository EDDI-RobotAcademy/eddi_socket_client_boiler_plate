from abc import ABC, abstractmethod


class CommandExecutorService(ABC):
    @abstractmethod
    def requestToInjectAnalyzerExecutorChannel(self, ipcAnalyzerExecutorChannel):
        pass

    @abstractmethod
    def requestToInjectExecutorTransmitterChannel(self, ipcExecutorTransmitterChannel):
        pass

    @abstractmethod
    def executeCommand(self):
        pass
