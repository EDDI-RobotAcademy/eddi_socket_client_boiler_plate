from abc import ABC, abstractmethod


class CommandExecutorRepository(ABC):
    @abstractmethod
    def execute(self):
        pass
