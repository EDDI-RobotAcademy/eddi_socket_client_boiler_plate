from abc import ABC, abstractmethod


class ResourceCheckRepository(ABC):

    @abstractmethod
    def parseMemoryInfo(self):
        pass
