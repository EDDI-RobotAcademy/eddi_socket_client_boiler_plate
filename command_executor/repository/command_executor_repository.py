from abc import ABC, abstractmethod


class CommandExecutorRepository(ABC):
    @abstractmethod
    def injectAnalyzerExecutorChannel(self, ipcAnalyzerExecutorChannel):
        pass

    @abstractmethod
    def injectExecutorTransmitter(self, ipcExecutorTransmitterChannel):
        pass

    @abstractmethod
    def execute(self):
        pass
