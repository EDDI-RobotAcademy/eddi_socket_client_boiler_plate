from parameter_test.repository.parameter_test_repository_impl import ParameterTestRepositoryImpl
from parameter_test.service.parameter_test_service import ParameterTestService


class ParameterTestServiceImpl(ParameterTestService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__parameterTestRepository = ParameterTestRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def useOneParameters(self, first):
        self.__parameterTestRepository.useOneParameters(first)

    def useTwoParameters(self, first, second):
        self.__parameterTestRepository.useTwoParameters(first, second)

    def useNParameters(self, *args, **kwargs):
        self.__parameterTestRepository.useNParameters(args, kwargs)
