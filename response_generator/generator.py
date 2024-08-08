from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from response_converter.converter import ResponseConverter
from response_generator.response_class_map import ResponseClassMap
from utility.color_print import ColorPrinter


class ResponseGenerator:
    @staticmethod
    def generate(protocol, response=None):
        protocolEnum = CustomProtocolNumber(protocol)
        responseClass = ResponseClassMap.getResponseClass(protocolEnum.name)

        if response is None:
            return None

        socketResponse = ResponseConverter.convert(response, responseClass)
        ColorPrinter.print_important_data("socketResponse", socketResponse)
        return socketResponse
