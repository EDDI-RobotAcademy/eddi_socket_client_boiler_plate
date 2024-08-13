from time import sleep

from transmitter.repository.transmitter_repository import TransmitterRepository


class TransmitterRepositoryImpl(TransmitterRepository):
    __instance = None
    __clientSocket = None
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

    def injectClientSocket(self, clientSocket):
        self.__clientSocket = clientSocket

    def injectExecutorTransmitterChannel(self, ipcExecutorTransmitterChannel):
        self.__ipcExecutorTransmitterChannel = ipcExecutorTransmitterChannel

    def getClientSocket(self):
        return self.__clientSocket

    def acquireWillBeTransmit(self):
        return self.__ipcExecutorTransmitterChannel.get()

    def transmit(self, clientSocketObject, serializedTransmitData):
        clientSocketObject.sendall(serializedTransmitData.encode())




