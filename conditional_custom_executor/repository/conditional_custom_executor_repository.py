from abc import ABC, abstractmethod


class ConditionalCustomExecutorRepository(ABC):
    @abstractmethod
    def injectExecutorConditionalCustomExecutorChannel(self, ipcExecutorConditionalCustomExecutorChannel):
        pass

    @abstractmethod
    def injectConditionalCustomExecutorTransmitterChannel(self, ipcConditionalCustomExecutorTransmitterChannel):
        pass

    @abstractmethod
    def acquireWillBeExecuteData(self):
        pass

    @abstractmethod
    def sendResponseToTransmitter(self, response):
        pass

    @abstractmethod
    def execute(self):
        pass
