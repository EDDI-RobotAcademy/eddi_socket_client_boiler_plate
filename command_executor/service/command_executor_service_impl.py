from command_executor.repository.command_executor_repository_impl import CommandExecutorRepositoryImpl
from command_executor.service.command_executor_service import CommandExecutorService
from utility.color_print import ColorPrinter


class CommandExecutorServiceImpl(CommandExecutorService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__commandExecutorRepository = CommandExecutorRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def execute_command(self):
        ColorPrinter.print_important_message("Command Executor 구동")
    