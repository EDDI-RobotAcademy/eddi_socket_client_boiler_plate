import socket

from decouple import config

from client_socket.entity.client_socket import ClientSocket
from client_socket.repository.client_socket_repository import ClientSocketRepository


class ClientSocketRepositoryImpl(ClientSocketRepository):
    __instance = None
    __clientSocket = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create(self):
        clientSocketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clientSocket = ClientSocket(config('TARGET_HOST'), int(config('TARGET_PORT')), clientSocketObject)
        return self.__clientSocket

    def connectToTargetHostUnitlSuccess(self):
        if not self.__clientSocket:
            self.create()
            
        clientSocketObject = self.__clientSocket.getSocket()
        
        try:
            clientSocketObject.connect(
                (
                    self.__clientSocket.getHost(),
                    self.__clientSocket.getPort(),
                )
            )
            
        except ConnectionRefusedError:
            print(f"{self.__clientSocket.getHost()}:{self.__clientSocket.getPort()} 연결 중 거절")

        except Exception as exception:
            print(f"연결 중 에러 발생: {str(exception)}")


