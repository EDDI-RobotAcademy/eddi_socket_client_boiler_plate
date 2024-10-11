from thread_worker.repository.thread_worker_repository_impl import ThreadWorkerRepositoryImpl
from thread_worker.service.thread_worker_service import ThreadWorkerService


class ThreadWorkerServiceImpl(ThreadWorkerService):
    __instance = None

    def __new__(cls, max_workers=8):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__threadWorkerRepository = ThreadWorkerRepositoryImpl.getInstance(max_workers=max_workers)
        return cls.__instance

    @classmethod
    def getInstance(cls, max_workers=8):
        if cls.__instance is None:
            cls.__instance = cls(max_workers=max_workers)
        return cls.__instance

    def createThreadWorker(self, name, willBeExecuteFunction):
        self.__threadWorkerRepository.save(name, willBeExecuteFunction)

    def executeThreadWorker(self, name):
        return self.__threadWorkerRepository.execute(name)

    def shutdown(self):
        self.__threadWorkerRepository.shutdown()
