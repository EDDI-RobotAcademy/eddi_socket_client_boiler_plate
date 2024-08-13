from abc import ABC, abstractmethod


class ClientSocketRepository(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def connectToTargetHostUnitSuccess(self):
        pass
