from abc import ABC, abstractmethod


class ConditionalCustomExecutorService(ABC):
    @abstractmethod
    def requestToInjectExecutorConditionalCustomExecutorChannel(self, ipcExecutorConditionalCustomExecutorChannel):
        pass

    @abstractmethod
    def requestToInjectConditionalCustomExecutorTransmitterChannel(self, ipcConditionalCustomExecutorTransmitterChannel):
        pass

    @abstractmethod
    def executeConditionalCustomCommand(self, conditionalCustomExecutorId):
        pass
