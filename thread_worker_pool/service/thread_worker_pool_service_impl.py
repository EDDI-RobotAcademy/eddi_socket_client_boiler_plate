from thread_worker.repository.thread_worker_repository_impl import ThreadWorkerRepositoryImpl
from thread_worker_pool.repository.thread_worker_pool_repository_impl import ThreadWorkerPoolRepositoryImpl
from thread_worker_pool.service.thread_worker_pool_service import ThreadWorkerPoolService


class ThreadWorkerPoolServiceImpl(ThreadWorkerPoolService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__threadWorkerPoolRepository = ThreadWorkerPoolRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createThreadWorkerPool(self, pipeline_stage: str, max_workers: int):
        self.__threadWorkerPoolRepository.createThreadWorkerPool(pipeline_stage, max_workers)

    def allocateExecuteFunction(self, pipeline_stage: str, function):
        self.__threadWorkerPoolRepository.allocateExecuteFunction(pipeline_stage, function)

    def executeThreadPoolWorker(self, pipeline_stage: str, *args):
        return self.__threadWorkerPoolRepository.executeThreadPoolWorker(pipeline_stage, *args)

    def shutdownPool(self, pipeline_stage: str):
        self.__threadWorkerPoolRepository.shutdownPool(pipeline_stage)

    def shutdownAll(self):
        self.__threadWorkerPoolRepository.shutdownAll()