from abc import ABC, abstractmethod


class ClientSocketService(ABC):
    @abstractmethod
    def createClientSocket(self):
        pass

    @abstractmethod
    def connectToTargetHostUnitSuccess(self):
        pass
