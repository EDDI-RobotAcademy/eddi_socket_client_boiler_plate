import multiprocessing

from task_worker.entity.task_worker import TaskWorker
from task_worker.repository.task_worker_repository import TaskWorkerRepository


class TaskWorkerRepositoryImpl(TaskWorkerRepository):
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
        taskWorker = TaskWorker(name, willBeExecuteFunction)
        self.__workerList[name] = taskWorker

    def execute(self, name):
        foundTaskWorker = self.__workerList[name]
        executeFunction = foundTaskWorker.getWillBeExecuteFunction()

        newTask = multiprocessing.Process(target=executeFunction)
        foundTaskWorker.setTaskPID(newTask.pid)

        newTask.start()
