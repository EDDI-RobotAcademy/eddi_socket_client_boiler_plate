from client_socket.repository.client_socket_repository_impl import ClientSocketRepositoryImpl
from client_socket.service.client_socket_service import ClientSocketService
from utility.color_print import ColorPrinter


class ClientSocketServiceImpl(ClientSocketService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__clientSocketRepository = ClientSocketRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createClientSocket(self):
        return self.__clientSocketRepository.create()

    def connectToTargetHostUnitSuccess(self):
        self.__clientSocketRepository.connectToTargetHostUnitSuccess()

        ColorPrinter.print_important_message("서버에 접속 성공!")

