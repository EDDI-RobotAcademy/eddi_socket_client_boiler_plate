from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from custom_protocol.repository.custom_protocol_repository import CustomProtocolRepository
from utility.color_print import ColorPrinter

try:
    from user_defined_protocol.protocol import UserDefinedProtocolNumber
except ImportError:
    UserDefinedProtocolNumber = None
    ColorPrinter.print_important_message("UserDefinedProtocolNumber는 사용자가 추가적인 프로토콜을 확장하기 위해 사용합니다.")


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
        print(f"Registering protocolNumber: {protocolNumber}, customFunction: {customFunction}")

        if protocolNumber is None:
            raise ValueError("프로토콜 번호가 None입니다.")
        if not (CustomProtocolNumber.hasValue(protocolNumber.value) or
                (UserDefinedProtocolNumber is not None and UserDefinedProtocolNumber.hasValue(protocolNumber.value))):
            raise ValueError("프로토콜을 등록 시 반드시 CustomProtocolNumber 혹은 UserDefinedProtocolNumber에 정의된 값을 사용하세요")
        if not callable(customFunction):
            raise  ValueError("customFunction은 프로토콜에 대응하는 함수입니다")

        self.__protocolTable[protocolNumber.value] = customFunction

    def execute(self, requestObject):
        ColorPrinter.print_important_data("CommandExecutor requestObject -> protocolNumber", requestObject.getProtocolNumber())
        ColorPrinter.print_important_data("customFunction", self.__protocolTable[requestObject.getProtocolNumber()])

        userDefinedFunction = self.__protocolTable[requestObject.getProtocolNumber()]

        if hasattr(requestObject, 'getParameterList') and callable(requestObject.getParameterList):
            parameterList = requestObject.getParameterList()
            ColorPrinter.print_important_data("parameterList", parameterList)
            if parameterList is not None:
                result = userDefinedFunction(*parameterList)
            else:
                result = userDefinedFunction()
        else:
            result = userDefinedFunction()

        ColorPrinter.print_important_data("result", result)

        return result
    