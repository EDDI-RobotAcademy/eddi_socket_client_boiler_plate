from receiver.repository.receiver_repository import ReceiverRepository
from utility.color_print import ColorPrinter


class ReceiverRepositoryImpl(ReceiverRepository):
    __instance = None
    __clientSocket = None

    SOCKET_BUFFER_SIZE = 2048

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getClientSocket(self):
        return self.__clientSocket

    def injectClientSocket(self, clientSocket):
        self.__clientSocket = clientSocket

    def receive(self):
        clientSocketObject = self.__clientSocket.getSocket()
        receivedData = clientSocketObject.recv(self.SOCKET_BUFFER_SIZE)
        return receivedData

    def closeConnection(self):
        ColorPrinter.print_important_message("Receiver 소켓 종료!")
        self.__clientSocket.closeSocket()
