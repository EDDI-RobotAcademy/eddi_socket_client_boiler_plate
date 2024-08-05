from abc import ABC, abstractmethod


class TransmitterService(ABC):
    @abstractmethod
    def requestToInjectClientSocket(self, clientSocket):
        pass

