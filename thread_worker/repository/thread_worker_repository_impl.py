import threading
from concurrent.futures import ThreadPoolExecutor

from thread_worker.entity.thread_worker import ThreadWorker
from thread_worker.repository.thread_worker_repository import ThreadWorkerRepository


class ThreadWorkerRepositoryImpl(ThreadWorkerRepository):
    __instance = None
    __workerList = {}

    __executor = None

    def __new__(cls, max_workers=8):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__executor = ThreadPoolExecutor(max_workers=max_workers)
        return cls.__instance

    @classmethod
    def getInstance(cls, max_workers=8):
        if cls.__instance is None:
            cls.__instance = cls(max_workers=max_workers)
        return cls.__instance

    def save(self, name, willBeExecuteFunction):
        theadWorker = ThreadWorker(name, willBeExecuteFunction)
        self.__workerList[name] = theadWorker

    def getWorker(self, name):
        return self.__workerList.get(name, None)

    def execute(self, name):
        foundThreadWorker = self.getWorker(name)
        if foundThreadWorker is None:
            raise ValueError(f"ThreadWorker with name '{name}' not found")

        executeFunction = foundThreadWorker.getWillBeExecuteFunction()

        future = self.__executor.submit(executeFunction)
        foundThreadWorker.setThreadId(future)

    def shutdown(self):
        if self.__executor:
            self.__executor.shutdown(wait=True)
