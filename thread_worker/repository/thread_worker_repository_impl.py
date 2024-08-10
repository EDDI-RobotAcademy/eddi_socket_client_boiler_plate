import threading

from thread_worker.entity.thread_worker import ThreadWorker
from thread_worker.repository.thread_worker_repository import ThreadWorkerRepository


class ThreadWorkerRepositoryImpl(ThreadWorkerRepository):
    __instance = None
    __workerList = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def save(self, name, willBeExecuteFunction):
        theadWorker = ThreadWorker(name, willBeExecuteFunction)
        self.__workerList[name] = theadWorker

    def execute(self, name):
        foundThreadWorker = self.__workerList[name]
        executeFunction = foundThreadWorker.getWillBeExecuteFunction()

        newThread = threading.Thread(target=executeFunction)
        newThread.start()

        foundThreadWorker.setThreadId(newThread.ident)
