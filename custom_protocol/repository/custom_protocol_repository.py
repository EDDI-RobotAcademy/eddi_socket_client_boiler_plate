from abc import ABC, abstractmethod


class CustomProtocolRepository(ABC):
    @abstractmethod
    def register(self, protocolNumber, customFunction):
        pass
