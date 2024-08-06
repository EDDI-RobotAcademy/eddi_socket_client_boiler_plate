from abc import ABC, abstractmethod


class CustomProtocolService(ABC):
    @abstractmethod
    def registerCustomProtocol(self, protocolNumber, customFunction):
        pass
    