class ThreadWorker:
    def __init__(self, name, willBeExecuteFunction):
        self.__threadId = None
        self.__name = name
        self.__willBeExecuteFunction = willBeExecuteFunction

    def setThreadId(self, threadId: int):
        self.__threadId = threadId

    def getThreadId(self) -> int:
        return self.__threadId

    def getName(self):
        return self.__name

    def getWillBeExecuteFunction(self):
        return self.__willBeExecuteFunction
