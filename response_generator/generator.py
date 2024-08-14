from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from response_converter.converter import ResponseConverter
from response_generator.response_class_map import ResponseClassMap
from utility.color_print import ColorPrinter

try:
    from user_defined_protocol.protocol import UserDefinedProtocolNumber
except ImportError:
    UserDefinedProtocolNumber = None
    ColorPrinter.print_important_message("UserDefinedProtocolNumber는 사용자가 추가적인 프로토콜을 확장하기 위해 사용합니다.")


class ResponseGenerator:
    __instance = None
    __responseClassMapInstance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectUserDefinedResponseClassMapInstance(self, responseClassMapInstance):
        self.__responseClassMapInstance = responseClassMapInstance

    def generate(self, protocolNumber, response=None):
        try:
            protocolEnum = CustomProtocolNumber(protocolNumber)

        except ValueError:
            if UserDefinedProtocolNumber is not None:
                try:
                    protocolEnum = UserDefinedProtocolNumber(protocolNumber)
                except ValueError:
                    ColorPrinter.print_important_data(
                        "CustomProtocolNumber 혹은 UserDefinedProtocolNumber에서 지원하지 않는 프로토콜입니다.")
            else:
                ColorPrinter.print_important_message("Socket Client는 CustomProtocolNumber만 지원하므로 DLLS-Client 구성을 하세요!")
                return None

        ColorPrinter.print_important_data("ResponseGenerator() protocolEnum", protocolEnum)

        # responseClass = ResponseClassMap.getResponseClass(protocolEnum.name)
        responseClass = self.__responseClassMapInstance.getResponseClass(protocolEnum.name)

        if response is None:
            return None

        socketResponse = ResponseConverter.convert(response, responseClass)
        ColorPrinter.print_important_data("socketResponse", socketResponse)
        return socketResponse
