import json
import socket
from time import sleep

from transmitter.repository.transmitter_repository_impl import TransmitterRepositoryImpl
from transmitter.service.transmitter_service import TransmitterService
from utility.color_print import ColorPrinter


class TransmitterServiceImpl(TransmitterService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__transmitterRepository = TransmitterRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectClientSocket(self, clientSocket):
        self.__transmitterRepository.injectClientSocket(clientSocket)

    def __blockToAcquireSocket(self):
        if self.__transmitterRepository.getClientSocket() is None:
            return True

        return False

    def requestToTransmitResult(self):
        while self.__blockToAcquireSocket():
            sleep(0.5)

        ColorPrinter.print_important_message("Transmitter 생성 성공!")

        while True:
            try:
                transmitData = "test"
                serializedData = json.dumps({"message": transmitData})

                # clientSocketObject.sendall(serializedData.encode())
                self.__transmitterRepository.transmit(serializedData)

            except (socket.error, BrokenPipeError) as exception:
                return None

            except socket.error as exception:
                print("전송 중 에러")

            except Exception as exception:
                print(f"Transmitter: {str(exception)}")

            finally:
                sleep(0.5)



