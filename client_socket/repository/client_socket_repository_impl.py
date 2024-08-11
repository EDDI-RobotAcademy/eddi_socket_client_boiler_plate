import errno
import select
import socket
import ssl

from decouple import config

from client_socket.entity.client_socket import ClientSocket
from client_socket.repository.client_socket_repository import ClientSocketRepository
from critical_section.manager import CriticalSectionManager
from ssl_tls.ssl_tls_context_manager import SslTlsClientContextManager


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
        SslTlsClientContextManager.initSslTlsContext()
        sslContext = SslTlsClientContextManager.getSSLContext()

        clientSocketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__setNonBlocking(clientSocketObject)

        sslClientSocket = sslContext.wrap_socket(clientSocketObject, server_side=False, server_hostname=config('TARGET_HOST'))

        self.__clientSocket = ClientSocket(config('TARGET_HOST'), int(config('TARGET_PORT')), sslClientSocket)
        critical_section_manager = CriticalSectionManager.getInstance()
        critical_section_manager.setClientSocket(self.__clientSocket)

        return self.__clientSocket

    def __setNonBlocking(self, socketObject):
        socketObject.setblocking(False)

    def connectToTargetHostUnitSuccess(self):
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

        except BlockingIOError as e:
            if e.errno != errno.EINPROGRESS:
                print(f"연결 중 에러 발생: {str(e)}")
                return
            print(f"연결 진행 중...")

        try:
            _, writable, _ = select.select([], [clientSocketObject], [], 10)
            if writable:
                print(f"{self.__clientSocket.getHost()}:{self.__clientSocket.getPort()} 연결 성공")
            else:
                print(f"{self.__clientSocket.getHost()}:{self.__clientSocket.getPort()} 연결 실패 (타임아웃)")

        except Exception as exception:
            print(f"연결 중 에러 발생: {str(exception)}")
