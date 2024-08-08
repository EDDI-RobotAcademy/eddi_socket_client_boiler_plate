import json
import socket
from time import sleep

from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from response_generator.generator import ResponseGenerator
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

    def requestToInjectExecutorTransmitterChannel(self, ipcExecutorTransmitterChannel):
        self.__transmitterRepository.injectExecutorTransmitterChannel(ipcExecutorTransmitterChannel)

    def __blockToAcquireSocket(self):
        if self.__transmitterRepository.getClientSocket() is None:
            return True

        return False

    def requestToTransmitResult(self):
        while self.__blockToAcquireSocket():
            sleep(0.5)

        ColorPrinter.print_important_message("Transmitter 구동 성공!")

        while True:
            try:
                willBeTransmitResponse = self.__transmitterRepository.acquireWillBeTransmit()
                ColorPrinter.print_important_data("Transmitter -> 전송할 데이터", willBeTransmitResponse)

                # transmitData = "test"
                # serializedData = json.dumps({"message": transmitData})

                # clientSocketObject.sendall(serializedData.encode())
                # TODO: Response Generator 만들어야함
                protocolNumber, response = willBeTransmitResponse
                socketResponse = ResponseGenerator.generate(protocolNumber, response)
                dictionarizedResponse = socketResponse.toDictionary()

                serializedRequestData = json.dumps(dictionarizedResponse, ensure_ascii=False)

                self.__transmitterRepository.transmit(serializedRequestData)

            except (socket.error, BrokenPipeError) as exception:
                return None

            except socket.error as exception:
                print("전송 중 에러")

            except Exception as exception:
                print(f"Transmitter: {str(exception)}")

            finally:
                sleep(0.5)



