from abc import ABC, abstractmethod


class ReceiverService(ABC):
    @abstractmethod
    def requestToInjectClientSocket(self, clientSocket):
        pass
