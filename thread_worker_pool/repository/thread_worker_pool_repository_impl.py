from concurrent.futures import ThreadPoolExecutor

from thread_worker_pool.entity.thread_worker_pool import ThreadWorkerPool
from thread_worker_pool.repository.thread_worker_pool_repository import ThreadWorkerPoolRepository
from utility.color_print import ColorPrinter


class ThreadWorkerPoolRepositoryImpl(ThreadWorkerPoolRepository):
    __instance = None
    __poolDictionary = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createThreadWorkerPool(self, pipeline_stage, max_workers):
        if pipeline_stage in self.__poolDictionary:
            raise ValueError(f"ThreadPool for {pipeline_stage} already exists.")

        executorPool = ThreadPoolExecutor(max_workers=max_workers)

        workerPool = ThreadWorkerPool(pipeline_stage, executorPool, max_workers)

        self.__poolDictionary[pipeline_stage] = {"executor": executorPool, "entity": workerPool}
        ColorPrinter.print_important_data("ThreadPool", pipeline_stage)
        ColorPrinter.print_important_data("created worker number", max_workers)

    def allocateExecuteFunction(self, pipeline_stage, willBeExecuteFunction):
        pool_info = self.__poolDictionary.get(pipeline_stage)
        if not pool_info:
            raise ValueError(f"No ThreadPool found for {pipeline_stage}")

        worker_pool = pool_info["entity"]
        worker_pool.setWillBeExecuteFunction(willBeExecuteFunction)
        ColorPrinter.print_important_data("ThreadPool allocateExecuteFunction", pipeline_stage)

    def getPool(self, pipeline_stage):
        if pipeline_stage not in self.__poolDictionary:
            raise ValueError(f"No ThreadPool found for {pipeline_stage}")
        return self.__poolDictionary[pipeline_stage]

    def shutdownPool(self, pipeline_stage):
        if pipeline_stage in self.__poolDictionary:
            self.__poolDictionary[pipeline_stage].shutdown(wait=True)
            ColorPrinter.print_important_data("Shutdown Threadpool worker", pipeline_stage)

            del self.__poolDictionary[pipeline_stage]
        else:
            raise ValueError(f"No ThreadPool found for {pipeline_stage}")

    def shutdownAll(self):
        for stage, pool_info in list(self.__poolDictionary.items()):
            executor = pool_info["executor"]
            executor.shutdown(wait=True)
            ColorPrinter.print_important_data("Shutdown every Threadpool worker", stage)
            del self.__poolDictionary[stage]

    def executeThreadPoolWorker(self, pipeline_stage, *args):
        ColorPrinter.print_important_data("ThreadPool started", pipeline_stage)
        pool_info = self.__poolDictionary.get(pipeline_stage)

        if not pool_info:
            raise ValueError(f"No ThreadWorkerPool found for {pipeline_stage}")

        pool = pool_info["executor"]
        worker_pool = pool_info["entity"]
        futures = []

        max_workers = worker_pool.getMaxWorkers()

        for i in range(max_workers):
            worker_func = worker_pool.getWillBeExecuteFunction()
            ColorPrinter.print_important_data("execute_thread_pool_worker() -> worker_func", worker_func)
            future = pool.submit(worker_func, i + 1, *args)
            ColorPrinter.print_important_data("execute_thread_pool_worker() -> future", future)
            worker_pool.setThreadId(future)
            futures.append(future)

        return futures
