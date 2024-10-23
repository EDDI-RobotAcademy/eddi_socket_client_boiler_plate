import queue
from time import sleep

from conditional_custom_executor.repository.conditional_custom_executor_repository_impl import \
    ConditionalCustomExecutorRepositoryImpl
from conditional_custom_executor.service.conditional_custom_executor_service import ConditionalCustomExecutorService
from custom_protocol.repository.custom_protocol_repository_impl import CustomProtocolRepositoryImpl
from utility.color_print import ColorPrinter


class ConditionalCustomExecutorServiceImpl(ConditionalCustomExecutorService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__conditionalCustomExecutorRepository = ConditionalCustomExecutorRepositoryImpl.getInstance()
            cls.__instance.__customProtocolRepository = CustomProtocolRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectExecutorConditionalCustomExecutorChannel(self, ipcExecutorConditionalCustomExecutorChannel):
        self.__conditionalCustomExecutorRepository.injectExecutorConditionalCustomExecutorChannel(ipcExecutorConditionalCustomExecutorChannel)

    def requestToInjectConditionalCustomExecutorTransmitterChannel(self, ipcConditionalCustomExecutorTransmitterChannel):
        self.__conditionalCustomExecutorRepository.injectConditionalCustomExecutorTransmitterChannel(ipcConditionalCustomExecutorTransmitterChannel)

    def executeConditionalCustomCommand(self, conditionalCustomExecutorId):
        ColorPrinter.print_important_message(f"ConditionalCustomExecutor-{conditionalCustomExecutorId} 구동 성공!")

        while True:
            try:
                conditionalTransmitData = self.__conditionalCustomExecutorRepository.acquireConditionalTransmitData()
                ColorPrinter.print_important_data(f"ConditionalCustomExecutor-{conditionalCustomExecutorId} -> 데이터", conditionalTransmitData)

                self.__conditionalCustomExecutorRepository.sendResponseToTransmitter(conditionalTransmitData)

            except queue.Empty:
                # ColorPrinter.print_important_message(f"ConditionalCustomExecutor-{conditionalCustomExecutorId}: 큐가 비어 있습니다. 데이터 대기 중...")
                sleep(0.2)

            except Exception as exception:
                ColorPrinter.print_important_message(f"ConditionalCustomExecutor-{conditionalCustomExecutorId} 실행 중 에러 발생: {str(exception)}")

            sleep(0.05)
