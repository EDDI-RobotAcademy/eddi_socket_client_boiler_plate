from custom_protocol.entity.default_protocol import DefaultProtocolNumber
from custom_protocol.repository.custom_protocol_repository import CustomProtocolRepository

try:
    from user_defined_protocol.entity.custom_protocol import CustomProtocolNumber
except ImportError:
    CustomProtocolNumber = None


class CustomProtocolRepositoryImpl(CustomProtocolRepository):
    __instance = None
    __protocolTable = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def register(self, protocolNumber, customFunction):
        if not isinstance(protocolNumber, DefaultProtocolNumber) and \
                (CustomProtocolNumber is None or not isinstance(protocolNumber, CustomProtocolNumber)):
            raise ValueError("프로토콜을 등록 할 시 반드시 FastAPI 쪽 user_defined_protocol에 정의하세요")
        if not callable(customFunction):
            raise  ValueError("customFunction은 프로토콜에 대응하는 함수입니다")

        self.__protocolTable[protocolNumber.value] = customFunction
    