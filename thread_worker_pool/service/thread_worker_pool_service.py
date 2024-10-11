# thread_worker_pool/service/thread_worker_pool_service.py

from abc import ABC, abstractmethod


class ThreadWorkerPoolService(ABC):

    @abstractmethod
    def createThreadWorkerPool(self, pipeline_stage: str, max_workers: int):
        pass

    @abstractmethod
    def allocateExecuteFunction(self, pipeline_stage: str, function):
        pass

    @abstractmethod
    def executeThreadPoolWorker(self, pipeline_stage: str, *args):
        pass

    @abstractmethod
    def shutdownPool(self, pipeline_stage: str):
        pass

    @abstractmethod
    def shutdownAll(self):
        pass
