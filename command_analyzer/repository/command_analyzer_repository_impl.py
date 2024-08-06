from abc import ABC, abstractmethod

from command_analyzer.repository.command_analyzer_repository import CommandAnalyzerRepository


class CommandAnalyzerRepositoryImpl(CommandAnalyzerRepository):
    __instance = None
    __ipcReceiverAnalyzerChannel = None
    __ipcAnalyzerExecutorChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def injectReceiverAnalyzerChannel(self, ipcReceiverAnalyzerChannel):
        self.__ipcReceiverAnalyzerChannel = ipcReceiverAnalyzerChannel

    def injectAnalyzerExecutorChannel(self, ipcAnalyzerExecutorChannel):
        self.__ipcAnalyzerExecutorChannel = ipcAnalyzerExecutorChannel

    def analysis(self):
        pass
    