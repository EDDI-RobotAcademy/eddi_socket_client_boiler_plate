from time import sleep

from command_executor.repository.command_executor_repository_impl import CommandExecutorRepositoryImpl
from command_executor.service.command_executor_service import CommandExecutorService
from custom_protocol.repository.custom_protocol_repository_impl import CustomProtocolRepositoryImpl
from utility.color_print import ColorPrinter


class CommandExecutorServiceImpl(CommandExecutorService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__commandExecutorRepository = CommandExecutorRepositoryImpl.getInstance()
            cls.__instance.__customProtocolRepository = CustomProtocolRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectAnalyzerExecutorChannel(self, ipcAnalyzerExecutorChannel):
        self.__commandExecutorRepository.injectAnalyzerExecutorChannel(ipcAnalyzerExecutorChannel)

    def requestToInjectExecutorTransmitterChannel(self, ipcExecutorTransmitterChannel):
        self.__commandExecutorRepository.injectExecutorTransmitter(ipcExecutorTransmitterChannel)

    def executeCommand(self):
        ColorPrinter.print_important_message("Command Executor 구동 성공!")

        while True:
            willBeExecuteData = self.__commandExecutorRepository.acquireWillBeExecuteData()
            ColorPrinter.print_important_data("Command Executor -> 실행할 데이터", willBeExecuteData)

            response = self.__customProtocolRepository.execute(willBeExecuteData)
            willBeTransmitDataTuple = (willBeExecuteData.getProtocolNumber(), response)
            self.__commandExecutorRepository.sendResponseToTransmitter(willBeTransmitDataTuple)

            sleep(0.5)