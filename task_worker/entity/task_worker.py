class TaskWorker:
    def __init__(self, name, willBeExecuteFunction):
        self.__taskPID = None
        self.__name = name
        self.__willBeExecuteFunction = willBeExecuteFunction

    def setTaskPID(self, taskPID: int):
        self.__taskPID = taskPID

    def getTaskPID(self) -> int:
        return self.__taskPID

    def getName(self):
        return self.__name

    def getWillBeExecuteFunction(self):
        return self.__willBeExecuteFunction