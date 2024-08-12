import threading
import socket
from utility.color_print import ColorPrinter

class CriticalSectionManager:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__clientSocket = None
            cls.__instance.__lock = threading.Lock()  # Lock 객체 생성
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def checkClientSocketIsNone(self):
        if self.__clientSocket is None:
            return False

        return True

    def setClientSocket(self, clientSocket):
        self.__clientSocket = clientSocket
        ColorPrinter.print_important_data("CriticalSectionManager -> setClientSocket", f"{clientSocket}")

    def getClientSocket(self):
        if self.__clientSocket is not None:
            ColorPrinter.print_important_data("CriticalSectionManager -> getClientSocket", f"{self.__clientSocket}")
            return self.__clientSocket
        else:
            self.clearClientSocket()  # 닫힌 소켓 제거
            return None

    def clearClientSocket(self):
        with self.__lock:  # Lock을 사용해 Critical Section 보호
            ColorPrinter.print_important_data("CriticalSectionManager -> clearClientSocket", f"Clearing socket: {self.__clientSocket}")
            self.__clientSocket = None
