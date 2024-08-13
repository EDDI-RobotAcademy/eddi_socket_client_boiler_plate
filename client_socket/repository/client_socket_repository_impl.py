import errno
import select
import socket
import ssl

from decouple import config

from client_socket.entity.client_socket import ClientSocket
from client_socket.repository.client_socket_repository import ClientSocketRepository
from critical_section.manager import CriticalSectionManager
from ssl_tls.ssl_tls_context_manager import SslTlsContextManager
from utility.color_print import ColorPrinter


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
        SslTlsContextManager.initSslTlsContext()
        sslContext = SslTlsContextManager.getSSLContext()

        clientSocketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__setNonBlocking(clientSocketObject)

        self.__clientSocket = ClientSocket(config('TARGET_HOST'), int(config('TARGET_PORT')), clientSocketObject)
        return self.__clientSocket

    def __setNonBlocking(self, socketObject):
        socketObject.setblocking(False)

    def connectToTargetHostUnitSuccess(self):
        if not self.__clientSocket:
            self.create()

        criticalSectionManager = CriticalSectionManager.getInstance()
        clientSocketObject = self.__clientSocket.getSocket()

        ColorPrinter.print_important_data("connectToTargetHostUnitSuccess()", clientSocketObject)

        try:
            clientSocketObject.connect(
                (
                    self.__clientSocket.getHost(),
                    self.__clientSocket.getPort(),
                )
            )
        except BlockingIOError:
            pass

        try:
            _, writable, _ = select.select([], [clientSocketObject], [], 10)
            if writable:
                ColorPrinter.print_important_message("연결 가능!")

                try:
                    sslContext = SslTlsContextManager.getSSLContext()
                    sslClientSocket = sslContext.wrap_socket(clientSocketObject,
                                                             server_side=False,
                                                             do_handshake_on_connect=False,
                                                             server_hostname=config('TARGET_HOST'))

                    if sslClientSocket is None:
                        raise ValueError("wrap_socket returned None")

                    # 핸드셰이크 시도
                    while True:
                        try:
                            ColorPrinter.print_important_message("SSL Handshake 시도!")
                            sslClientSocket.do_handshake()
                            ColorPrinter.print_important_message("SSL Handshake Success!")
                            criticalSectionManager.setClientSocket(sslClientSocket)
                            break

                        except ssl.SSLWantReadError:
                            select.select([sslClientSocket], [], [])
                        except ssl.SSLWantWriteError:
                            select.select([], [sslClientSocket], [])
                        except ssl.SSLError as sslError:
                            ColorPrinter.print_important_data("SSL Handshake Error!", str(sslError))
                            sslClientSocket.close()
                            self.__clientSocket = None
                            return

                except ssl.SSLError as sslError:
                    ColorPrinter.print_important_data("SSL Error during wrap_socket or handshake!", str(sslError))
                    clientSocketObject.close()
                    self.__clientSocket = None

            else:
                print(f"{self.__clientSocket.getHost()}:{self.__clientSocket.getPort()} 연결 실패 (타임아웃)")
                self.__clientSocket = None

        except Exception as exception:
            print(f"연결 중 에러 발생: {str(exception)}")
            if clientSocketObject:
                clientSocketObject.close()
            self.__clientSocket = None
