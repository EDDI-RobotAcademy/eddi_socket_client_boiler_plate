from time import sleep

from command_analyzer.repository.command_analyzer_repository_impl import CommandAnalyzerRepositoryImpl
from command_analyzer.service.command_analyzer_service import CommandAnalyzerService
from protocol_validation.validator import ProtocolValidator
from utility.color_print import ColorPrinter


class CommandAnalyzerServiceImpl(CommandAnalyzerService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__commandAnalyzerRepository = CommandAnalyzerRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectReceiverAnalyzerChannel(self, ipcReceiverAnalyzerChannel):
        self.__commandAnalyzerRepository.injectReceiverAnalyzerChannel(ipcReceiverAnalyzerChannel)

    def requestToInjectAnalyzerExecutorChannel(self, ipcAnalyzerExecutorChannel):
        self.__commandAnalyzerRepository.injectAnalyzerExecutorChannel(ipcAnalyzerExecutorChannel)

    def analysisCommand(self):
        ColorPrinter.print_important_message("Command Analyzer 구동 성공!")

        while True:
            needToAnalysisRequestedData = self.__commandAnalyzerRepository.acquireNeedToAnalysisRequestedData()
            ColorPrinter.print_important_data("Command Analyzer -> 분석할 데이터", needToAnalysisRequestedData)

            if ProtocolValidator.validate(needToAnalysisRequestedData):
                self.__commandAnalyzerRepository.sendDataToCommandExecutor(needToAnalysisRequestedData)

            sleep(1)
    