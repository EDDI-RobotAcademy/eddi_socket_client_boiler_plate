from abc import ABC, abstractmethod


class TransmitterRepository(ABC):
    @abstractmethod
    def injectClientSocket(self, clientSocket):
        pass

    @abstractmethod
    def requestToTransmitResult(self):
        pass

    @abstractmethod
    def transmit(self, serializedTransmitData):
        pass
