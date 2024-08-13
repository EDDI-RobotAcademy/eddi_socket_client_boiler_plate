from abc import ABC, abstractmethod

from parameter_test.repository.parameter_test_repository import ParameterTestRepository
from utility.color_print import ColorPrinter


class ParameterTestRepositoryImpl(ParameterTestRepository):
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

    def useOneParameters(self, first):
        ColorPrinter.print_important_data("first", first)
        return 1

    def useTwoParameters(self, first, second):
        ColorPrinter.print_important_data("first", first)
        ColorPrinter.print_important_data("second", second)
        return 2

    def useNParameters(self, *args, **kwargs):
        totalParameters = len(args) + len(kwargs)

        ColorPrinter.print_important_data("totalParameters", totalParameters)
        ColorPrinter.print_important_data("args", args)
        ColorPrinter.print_important_data("kwargs", kwargs)

        return totalParameters
    