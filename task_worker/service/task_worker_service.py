from abc import ABC, abstractmethod


class TaskWorkerService(ABC):
    @abstractmethod
    def createTaskWorker(self, name, willBeExecuteFunction):
        pass

    @abstractmethod
    def executeTaskWorker(self, name):
        pass
