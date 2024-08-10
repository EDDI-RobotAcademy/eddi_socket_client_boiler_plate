from abc import ABC, abstractmethod


class ThreadWorkerService(ABC):
    @abstractmethod
    def createThreadWorker(self, name, willBeExecuteFunction):
        pass

    @abstractmethod
    def executeThreadWorker(self, name):
        pass
