class ThreadWorkerPool:
    def __init__(self, name, executorPool, maxWorkers):
        self.name = name
        self.executorPool = executorPool
        self.willBeExecuteFunction = None
        self.maxWorkers = maxWorkers
        self.threadId = None

    def getName(self):
        return self.name

    def getMaxWorkers(self):
        return self.maxWorkers

    def setWillBeExecuteFunction(self, willBeExecuteFunction):
        self.willBeExecuteFunction = willBeExecuteFunction

    def getWillBeExecuteFunction(self):
        return self.willBeExecuteFunction

    def getExecutorPool(self):
        return self.executorPool

    def setThreadId(self, future):
        self.threadId = future

    def getThreadId(self):
        return self.threadId
