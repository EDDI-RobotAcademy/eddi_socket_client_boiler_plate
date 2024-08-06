from ipc_queue.repository.ipc_queue_repository_impl import IPCQueueRepositoryImpl
from ipc_queue.service.ipc_queue_service import IPCQueueService


class IPCQueueServiceImpl(IPCQueueService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createEssentialIPCQueue(self):
        self.__ipcQueueRepository.createEssentialIPCQueue()
    