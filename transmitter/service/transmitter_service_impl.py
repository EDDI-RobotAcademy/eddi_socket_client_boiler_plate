import json
import socket
import threading
from time import sleep

from critical_section.manager import CriticalSectionManager
from response_generator.generator import ResponseGenerator
from response_generator.packet_length_response import PacketLengthResponse
from transmitter.repository.transmitter_repository_impl import TransmitterRepositoryImpl
from transmitter.service.transmitter_service import TransmitterService
from utility.color_print import ColorPrinter


class TransmitterServiceImpl(TransmitterService):
    __instance = None

    __responseClassMapInstance = None
    __responseGeneratorInstance = ResponseGenerator.getInstance()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__transmitterRepository = TransmitterRepositoryImpl.getInstance()

            cls.__instance.__criticalSectionManager = CriticalSectionManager.getInstance()

            cls.__instance.__transmitterLock = threading.Lock()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectUserDefinedResponseClassMapInstance(self, responseClassMapInstance):
        self.__responseClassMapInstance = responseClassMapInstance
        self.__responseGeneratorInstance.requestToInjectUserDefinedResponseClassMapInstance(responseClassMapInstance)

    def requestToInjectClientSocket(self, clientSocket):
        self.__transmitterRepository.injectClientSocket(clientSocket)

    def requestToInjectExecutorTransmitterChannel(self, ipcExecutorTransmitterChannel):
        self.__transmitterRepository.injectExecutorTransmitterChannel(ipcExecutorTransmitterChannel)

    # def __blockToAcquireSocket(self):
    #     if self.__transmitterRepository.getClientSocket() is None:
    #         return True
    #
    #     return False

    # def __sendFixedLengthHeader(self, clientSocketObject, protocolNumber, data):
    #     # 데이터 직렬화
    #     serialized_data = json.dumps(data, ensure_ascii=False)
    #     data_length = len(serialized_data)
    #
    #     # 고정된 크기의 헤더 생성 (16바이트: 8바이트 프로토콜 번호 + 8바이트 데이터 길이)
    #     protocolNumber_str = str(protocolNumber).ljust(8)  # 8바이트로 맞추기
    #     packetDataLength_str = str(data_length).ljust(8)  # 8바이트로 맞추기
    #     header = f"{protocolNumber_str}{packetDataLength_str}".encode('utf-8')  # 헤더 생성
    #
    #     # 헤더와 데이터 전송
    #     with threading.Lock():  # 동기화
    #         clientSocketObject.sendall(header + serialized_data.encode('utf-8'))

    def __transmitInChunks(self, clientSocketObject, data, chunkSize=4096):
        total_length = len(data)
        sent_length = 0

        while sent_length < total_length:
            chunk = data[sent_length:sent_length + chunkSize]
            clientSocketObject.sendall(chunk.encode('utf-8'))
            sent_length += len(chunk)
            ColorPrinter.print_important_data("송신한 청크 길이", len(chunk))

            sleep(0.1)

        ColorPrinter.print_important_message("모든 청크 전송 완료")

    def __blockToAcquireSocket(self):
        if self.__criticalSectionManager.getClientSocket() is None:
            return True

        return False

    def requestToTransmitResult(self):
        while self.__blockToAcquireSocket():
            ColorPrinter.print_important_message("Transmitter: Try to get SSL Socket")
            sleep(0.5)

        ColorPrinter.print_important_message("Transmitter 구동 성공!")

        clientSocketObject = self.__criticalSectionManager.getClientSocket()
        ColorPrinter.print_important_data("requestToTransmitResult() -> clientSocketObject", clientSocketObject)

        while True:
            try:
                willBeTransmitResponse = self.__transmitterRepository.acquireWillBeTransmit()
                # ColorPrinter.print_important_data("Transmitter -> 전송할 데이터", willBeTransmitResponse)

                protocolNumber, response = willBeTransmitResponse
                socketResponse = self.__responseGeneratorInstance.generate(protocolNumber, response)
                # socketResponse = ResponseGenerator.generate(protocolNumber, response)

                if socketResponse is None:
                    continue

                if clientSocketObject.fileno() == -1:  # 소켓이 유효한지 확인
                    raise socket.error("Socket is closed or invalid")

                dictionarizedResponse = socketResponse.toDictionary()
                serializedRequestData = json.dumps(dictionarizedResponse, ensure_ascii=False)
                utf8EncodedRequestData = serializedRequestData.encode("utf-8")

                # TODO: 전체 패킷 길이를 계산해야함
                # 계산하여 수신측이 지속적으로 정보를 수신할 수 있도록 만들어야함
                # 길이 계산이 잘못되고 있음
                packetLength = len(utf8EncodedRequestData)
                # ColorPrinter.print_important_data("전체 패킷 길이", packetLength)

                # 일관성 유지를 위해 PacketLengthResponse를 구성하도록 만든다.
                packetLengthResponse = PacketLengthResponse(packetLength)
                dictionarizedPacketLengthResponse = packetLengthResponse.toFixedSizeDictionary()
                serializedPacketLengthData = json.dumps(dictionarizedPacketLengthResponse, ensure_ascii=False)
                # ColorPrinter.print_important_data("utf8EncodedRequestData", utf8EncodedRequestData)
                ColorPrinter.print_important_data("패킷 길이 응답", serializedPacketLengthData)
                ColorPrinter.print_important_data("패킷 길이 객체의 길이", len(serializedPacketLengthData))

                with self.__transmitterLock:
                    # 전체 패킷 길이 전송
                    self.__transmitterRepository.transmit(clientSocketObject, serializedPacketLengthData)
                    # 실제 내용물 전송
                    # self.__transmitterRepository.transmit(clientSocketObject, serializedRequestData)
                    self.__transmitInChunks(clientSocketObject, serializedRequestData)

            except (socket.error, BrokenPipeError) as exception:
                return None

            except socket.error as exception:
                print("전송 중 에러")

            except Exception as exception:
                print(f"Transmitter: {str(exception)}")

            finally:
                sleep(0.5)



