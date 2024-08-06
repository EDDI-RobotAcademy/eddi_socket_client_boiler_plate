import socket
from time import sleep

from receiver.repository.receiver_repository_impl import ReceiverRepositoryImpl
from receiver.service.receiver_service import ReceiverService
from request_generator.generator import RequestGenerator
from utility.color_print import ColorPrinter


class ReceiverServiceImpl(ReceiverService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__receiverRepository = ReceiverRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectClientSocket(self, clientSocket):
        self.__receiverRepository.injectClientSocket(clientSocket)

    def requestToInjectReceiverAnalyzerChannel(self, ipcReceiverAnalyzerChannel):
        self.__receiverRepository.injectReceiverAnalyzerChannel(ipcReceiverAnalyzerChannel)

    def __blockToAcquireSocket(self):
        if self.__receiverRepository.getClientSocket() is None:
            return True

        return False

    def requestToReceiveCommand(self):
        while self.__blockToAcquireSocket():
            sleep(0.5)

        ColorPrinter.print_important_message("Receiver 생성 성공!")

        while True:
            try:
                receivedData = self.__receiverRepository.receive()

                if not receivedData:
                    self.__receiverRepository.closeConnection()
                    break

                decodedData = receivedData.decode()
                ColorPrinter.print_important_data("수신된 정보", decodedData)

                requestData = RequestGenerator.generate(decodedData)

                self.__receiverRepository.sendDataToCommandAnalyzer(requestData)

            except BlockingIOError:
                pass

            except (socket.error, BrokenPipeError) as exception:
                ColorPrinter.print_important_message("Broken Pipe")
                self.__receiverRepository.closeConnection()
                break

            except socket.error as socketException:
                if socketException.errno == socket.errno.EAGAIN == socket.errno.EWOULDBLOCK:
                    ColorPrinter.print_important_message("문제 없음")
                    sleep(0.5)

                else:
                    ColorPrinter.print_important_message("수신 중 에러")

            except Exception as exception:
                ColorPrinter.print_important_data("Receiver 정보", str(exception))

            finally:
                sleep(0.5)

