from abc import ABC, abstractmethod

from command_analyzer.repository.command_analyzer_repository import CommandAnalyzerRepository


class CommandAnalyzerRepositoryImpl(CommandAnalyzerRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def analysis(self):
        pass
    