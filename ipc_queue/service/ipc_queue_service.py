from abc import ABC, abstractmethod


class IPCQueueService(ABC):
    @abstractmethod
    def createEssentialIPCQueue(self):
        pass
