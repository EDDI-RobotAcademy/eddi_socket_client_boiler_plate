from abc import ABC, abstractmethod


class ResourceCheckService(ABC):

    @abstractmethod
    def checkMemoryResource(self):
        pass
