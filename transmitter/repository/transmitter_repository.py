from abc import ABC, abstractmethod


class TransmitterRepository(ABC):
    @abstractmethod
    def injectClientSocket(self, clientSocket):
        pass

    @abstractmethod
    def injectExecutorTransmitterChannel(self, ipcExecutorTransmitterChannel):
        pass

    @abstractmethod
    def acquireWillBeTransmit(self):
        pass

    @abstractmethod
    def transmit(self, clientSocketObject, serializedTransmitData):
        pass
