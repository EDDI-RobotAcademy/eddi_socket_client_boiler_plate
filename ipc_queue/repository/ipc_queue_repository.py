from abc import ABC, abstractmethod


class IPCQueueRepository(ABC):
    @abstractmethod
    def createEssentialIPCQueue(self):
        pass
