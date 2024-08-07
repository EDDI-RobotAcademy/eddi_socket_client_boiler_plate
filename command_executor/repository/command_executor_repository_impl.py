from command_executor.repository.command_executor_repository import CommandExecutorRepository


class CommandExecutorRepositoryImpl(CommandExecutorRepository):
    __instance = None
    __ipcAnalyzerExecutorChannel = None
    __ipcExecutorTransmitterChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def injectAnalyzerExecutorChannel(self, ipcAnalyzerExecutorChannel):
        self.__ipcAnalyzerExecutorChannel = ipcAnalyzerExecutorChannel

    def injectExecutorTransmitter(self, ipcExecutorTransmitterChannel):
        self.__ipcExecutorTransmitterChannel = ipcExecutorTransmitterChannel

    def acquireWillBeExecuteData(self):
        return self.__ipcAnalyzerExecutorChannel.get()

    def sendResponseToTransmitter(self, response):
        self.__ipcExecutorTransmitterChannel.put(response)

    def execute(self):
        pass
    