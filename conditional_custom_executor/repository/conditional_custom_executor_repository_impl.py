from abc import ABC, abstractmethod

from conditional_custom_executor.repository.conditional_custom_executor_repository import \
    ConditionalCustomExecutorRepository


class ConditionalCustomExecutorRepositoryImpl(ConditionalCustomExecutorRepository):
    __instance = None
    __ipcExecutorConditionalCustomExecutorChannel = None
    __ipcConditionalCustomExecutorTransmitterChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def injectExecutorConditionalCustomExecutorChannel(self, ipcExecutorConditionalCustomExecutorChannel):
        self.__ipcExecutorConditionalCustomExecutorChannel = ipcExecutorConditionalCustomExecutorChannel

    def injectConditionalCustomExecutorTransmitterChannel(self, ipcConditionalCustomExecutorTransmitterChannel):
        self.__ipcConditionalCustomExecutorTransmitterChannel = ipcConditionalCustomExecutorTransmitterChannel

    def acquireConditionalTransmitData(self):
        return self.__ipcExecutorConditionalCustomExecutorChannel.get(False)

    def sendResponseToTransmitter(self, response):
        self.__ipcConditionalCustomExecutorTransmitterChannel.put(response)

    def execute(self):
        pass
