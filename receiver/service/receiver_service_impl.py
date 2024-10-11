import errno
import json
import socket
import ssl
import threading
from time import sleep

import select

from critical_section.manager import CriticalSectionManager
from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from receiver.repository.receiver_repository_impl import ReceiverRepositoryImpl
from receiver.service.receiver_service import ReceiverService
from request_generator.generator import RequestGenerator
from request_generator.request_class_map import RequestClassMap
from utility.color_print import ColorPrinter

try:
    from user_defined_protocol.protocol import UserDefinedProtocolNumber
except ImportError:
    UserDefinedProtocolNumber = None
    ColorPrinter.print_important_message("UserDefinedProtocolNumber는 사용자가 추가적인 프로토콜을 확장하기 위해 사용합니다.")


class ReceiverServiceImpl(ReceiverService):
    __instance = None

    __requestClassMapInstance = None
    __requestGeneratorInstance = RequestGenerator.getInstance()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__receiverRepository = ReceiverRepositoryImpl.getInstance()

            cls.__instance.__criticalSectionManager = CriticalSectionManager.getInstance()

            cls.__instance.__receiverLock = threading.Lock()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectUserDefinedRequestClassMapInstance(self, requestClassMapInstance):
        self.__requestClassMapInstance = requestClassMapInstance
        self.__requestGeneratorInstance.requestToInjectUserDefinedRequestClassMapInstance(requestClassMapInstance)

    def requestToInjectClientSocket(self, clientSocket):
        self.__receiverRepository.injectClientSocket(clientSocket)

    def requestToInjectReceiverAnalyzerChannel(self, ipcReceiverAnalyzerChannel):
        self.__receiverRepository.injectReceiverAnalyzerChannel(ipcReceiverAnalyzerChannel)

    def __recvFixedLength(self, clientSocketObject, length):
        data = b''
        remaining = length

        while remaining > 0:
            try:
                chunk = clientSocketObject.recv(remaining)
                if not chunk:
                    raise ConnectionError("Socket connection lost")
                data += chunk
                remaining -= len(chunk)
            except ssl.SSLWantReadError:
                continue
        return data

    def __blockToAcquireSocket(self):
        if self.__criticalSectionManager.getClientSocket() is None:
            return True

        return False

    def requestToReceiveCommand(self, receiverId):
        while self.__blockToAcquireSocket():
            ColorPrinter.print_important_message(f"Receiver-{receiverId}: Try to get SSL Socket")
            sleep(0.5)

        ColorPrinter.print_important_message(f"Receiver-{receiverId} 구동 성공!")

        clientSocketObject = self.__criticalSectionManager.getClientSocket()
        ColorPrinter.print_important_data(f"Receiver-{receiverId} requestToReceiveCommand() -> clientSocketObject", clientSocketObject)

        while True:
            try:
                with self.__receiverLock:
                    readyToRead, _, inError = select.select([clientSocketObject], [], [], 0.5)

                    if not readyToRead:
                        continue

                    headerData = self.__recvFixedLength(clientSocketObject, 58)
                    ColorPrinter.print_important_data(f"Receiver-{receiverId} headerData", headerData)

                    parsedHeaderData = json.loads(headerData)
                    protocolNumber = int(parsedHeaderData.get("protocolNumber"))
                    packetDataLength = int(parsedHeaderData.get("packetDataLength").strip())
                    # ColorPrinter.print_important_data(f"Receiver-{receiverId} protocolNumber", protocolNumber)
                    # ColorPrinter.print_important_data(f"Receiver-{receiverId} packetDataLength", packetDataLength)

                    receivedData = self.__recvFixedLength(clientSocketObject, packetDataLength)

                if not receivedData:
                    ColorPrinter.print_important_message(f"Receiver-{receiverId} 빈 데이터 수신, 연결을 종료합니다.")
                    self.__receiverRepository.closeConnection()
                    break

                # 수신한 데이터가 유효한 JSON인지 확인
                try:
                    dictionaryData = json.loads(receivedData)
                    # ColorPrinter.print_important_data(f"Receiver-{receiverId} dictionaryData", dictionaryData)

                except json.JSONDecodeError as e:
                    ColorPrinter.print_important_data(f"Receiver-{receiverId} JSON Decode Error: 수신된 데이터가 JSON 형식이 아닙니다", str(e))
                    continue

                protocolNumber = dictionaryData.get("command")
                # ColorPrinter.print_important_data(f"Receiver-{receiverId} protocolNumber", protocolNumber)

                data = dictionaryData.get("data", {})
                # ColorPrinter.print_important_data(f"Receiver-{receiverId} data", data)

                if protocolNumber is not None:
                    # ColorPrinter.print_important_data(f"Receiver-{receiverId} received protocol",
                    #                                   f"Protocol Number: {protocolNumber}, Data: {data}")

                    try:
                        protocol = CustomProtocolNumber(protocolNumber)

                    except ValueError:
                        if UserDefinedProtocolNumber is not None:
                            try:
                                protocol = UserDefinedProtocolNumber(protocolNumber)
                            except ValueError:
                                ColorPrinter.print_important_data(f"Receiver-{receiverId} CustomProtocolNumber 혹은 UserDefinedProtocolNumber에서 지원하지 않는 프로토콜입니다.")
                        else:
                            ColorPrinter.print_important_message(f"Receiver-{receiverId} Socket Client는 CustomProtocolNumber만 지원하므로 DLLS-Client 구성을 하세요!")
                            continue

                    request = self.__requestGeneratorInstance.generate(protocol, data)
                    ColorPrinter.print_important_data(f"Receiver-{receiverId} processed request", f"{request}")

                    self.__receiverRepository.sendDataToCommandAnalyzer(request)

            except ssl.SSLWantReadError:
                select.select([clientSocketObject], [], [])
                continue

            except ssl.SSLWantWriteError:
                select.select([], [clientSocketObject], [])
                continue

            except ssl.SSLError as sslError:
                ColorPrinter.print_important_data(f"Receiver-{receiverId} receive 중 SSL Error", str(sslError))
                self.__receiverRepository.closeConnection()
                break

            except BlockingIOError:
                pass

            except socket.error as socketException:
                if socketException.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                    ColorPrinter.print_important_message(f"Receiver-{receiverId} 문제 없음")
                    sleep(0.2)
                else:
                    ColorPrinter.print_important_message(f"Receiver-{receiverId} 수신 중 에러")
                    self.__receiverRepository.closeConnection()
                    break

            except (socket.error, BrokenPipeError) as exception:
                ColorPrinter.print_important_message(f"Receiver-{receiverId} Broken Pipe")
                self.__receiverRepository.closeConnection()
                break

            except Exception as exception:
                ColorPrinter.print_important_data(f"Receiver-{receiverId} Exception 정보", str(exception))

            finally:
                sleep(0.2)
