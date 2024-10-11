from abc import ABC, abstractmethod


class TransmitterService(ABC):
    @abstractmethod
    def requestToInjectClientSocket(self, clientSocket):
        pass

    @abstractmethod
    def requestToInjectExecutorTransmitterChannel(self, ipcExecutorTransmitterChannel):
        pass

    @abstractmethod
    def requestToTransmitResult(self, transmitterId):
        pass
