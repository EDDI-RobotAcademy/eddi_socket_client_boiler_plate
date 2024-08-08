from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from response_converter.converter import ResponseConverter
from response_generator.response_class_map import ResponseClassMap
from utility.color_print import ColorPrinter


class ResponseGenerator:
    @staticmethod
    def generate(protocol, response=None):
        protocolEnum = CustomProtocolNumber(protocol)
        responseClass = ResponseClassMap.getResponseClass(protocolEnum.name)
        # TODO: 다른 상황에서도 사용할 수 있도록 일반화 시켜야함
        # if responseClass:
        #     if response:
        #         socketResponse = ResponseConverter.convert(response, responseClass)
        #         ColorPrinter.print_important_data("socketResponse", socketResponse)
        #         return socketResponse
        #     else:
        #         return responseClass()

        if responseClass:
            socketResponse = ResponseConverter.convert(response, responseClass)
            ColorPrinter.print_important_data("socketResponse", socketResponse)
            return socketResponse

        raise ValueError("서포트하지 않는 Response Type 입니다")
