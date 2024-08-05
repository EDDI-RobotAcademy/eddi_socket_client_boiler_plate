from abc import ABC, abstractmethod


class TransmitterRepository(ABC):
    @abstractmethod
    def injectClientSocket(self, clientSocket):
        pass
