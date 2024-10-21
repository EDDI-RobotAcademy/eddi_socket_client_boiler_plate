from time import sleep

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
            willBeExecuteData = self.__conditionalCustomExecutorRepository.acquireWillBeExecuteData()
            ColorPrinter.print_important_data(f"ConditionalCustomExecutor-{conditionalCustomExecutorId} -> 실행할 데이터", willBeExecuteData)

            response = self.__conditionalCustomExecutorRepository.execute(willBeExecuteData)
            willBeTransmitDataTuple = (willBeExecuteData.getProtocolNumber(), response)
            self.__conditionalCustomExecutorRepository.sendResponseToTransmitter(willBeTransmitDataTuple)

            sleep(0.2)
