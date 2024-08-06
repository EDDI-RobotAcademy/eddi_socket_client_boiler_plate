from command_executor.service.command_executor_service import CommandExecutorService


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
        pass
    