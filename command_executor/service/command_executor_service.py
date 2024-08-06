from abc import ABC, abstractmethod


class CommandExecutorService(ABC):
    @abstractmethod
    def execute_command(self):
        pass
