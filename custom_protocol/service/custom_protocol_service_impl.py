from custom_protocol.repository.custom_protocol_repository_impl import CustomProtocolRepositoryImpl
from custom_protocol.service.custom_protocol_service import CustomProtocolService


class CustomProtocolServiceImpl(CustomProtocolService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__customProtocolRepository = CustomProtocolRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def registerCustomProtocol(self, protocolNumber, customFunction):
        self.__customProtocolRepository.register(protocolNumber, customFunction)

