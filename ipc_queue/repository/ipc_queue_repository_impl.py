import multiprocessing

from ipc_queue.repository.ipc_queue_repository import IPCQueueRepository


class IPCQueueRepositoryImpl(IPCQueueRepository):
    __instance = None

    __ipcReceiverAnalyzerChannel = None
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

    def getIPCReceiverAnalyzerChannel(self):
        return self.__ipcReceiverAnalyzerChannel

    def getIPCAnalyzerExecutorChannel(self):
        return self.__ipcAnalyzerExecutorChannel

    def getIPCExecutorTransmitterChannel(self):
        return self.__ipcExecutorTransmitterChannel

    def createEssentialIPCQueue(self):
        self.__ipcReceiverAnalyzerChannel = multiprocessing.Queue()
        self.__ipcAnalyzerExecutorChannel = multiprocessing.Queue()
        self.__ipcExecutorTransmitterChannel = multiprocessing.Queue()
    