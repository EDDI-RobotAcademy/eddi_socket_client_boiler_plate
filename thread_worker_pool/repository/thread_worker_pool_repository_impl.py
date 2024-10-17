import asyncio
import concurrent
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from thread_worker_pool.entity.thread_worker_pool import ThreadWorkerPool
from thread_worker_pool.repository.thread_worker_pool_repository import ThreadWorkerPoolRepository
from utility.color_print import ColorPrinter


class ThreadWorkerPoolRepositoryImpl(ThreadWorkerPoolRepository):
    __instance = None
    __poolDictionary = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.executor = concurrent.futures.ThreadPoolExecutor()
            cls.__instance.lock = threading.Lock()

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
        pool_info = self.__poolDictionary.get(pipeline_stage)
        if pool_info:
            executor = pool_info["executor"]
            worker_pool = pool_info["entity"]

            executor.shutdown(wait=True)
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

    def executeThreadPoolWorker(self, worker_name, worker_func, *args):
        ColorPrinter.print_important_message(f"Starting {worker_name} worker thread.")

        try:
            # 스레드 풀에서 작업을 제출합니다.
            future = self.executor.submit(worker_func, *args)
            future.add_done_callback(self.thread_completed_callback)  # 작업 완료 시 호출되는 콜백 추가
        except Exception as e:
            ColorPrinter.print_important_message(f"Failed to start {worker_name}: {e}")

    def thread_completed_callback(self, future):
        try:
            result = future.result()  # 작업 결과를 가져옵니다.
            ColorPrinter.print_important_message(f"Thread completed with result: {result}")
        except Exception as e:
            ColorPrinter.print_important_message(f"Thread failed with exception: {e}")

    def shutdown(self):
        ColorPrinter.print_important_message("Shutting down thread pool.")
        self.executor.shutdown(wait=True)