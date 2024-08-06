from command_analyzer.repository.command_analyzer_repository_impl import CommandAnalyzerRepositoryImpl
from command_analyzer.service.command_analyzer_service import CommandAnalyzerService
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

    def analysisCommand(self):
        ColorPrinter.print_important_message("Command Analyzer 구동")
    