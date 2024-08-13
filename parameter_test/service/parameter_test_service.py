from abc import ABC, abstractmethod


class ParameterTestService(ABC):
    @abstractmethod
    def useOneParameters(self, first):
        pass

    @abstractmethod
    def useTwoParameters(self, first, second):
        pass

    @abstractmethod
    def useNParameters(self, *args, **kwargs):
        pass
