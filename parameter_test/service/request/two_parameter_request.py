from request_generator.base_request import BaseRequest
from request_generator.request_type import RequestType
from utility.color_print import ColorPrinter


class TwoParametersRequest(BaseRequest):
    def __init__(self, **kwargs):
        self.__protocolNumber = RequestType.TWO_PARAMETERS.value
        ColorPrinter.print_important_data("kwargs", kwargs)
        self.parameterList = kwargs.get('data', [])

    def getProtocolNumber(self):
        return self.__protocolNumber

    def getParameterList(self):
        return tuple(self.parameterList)

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "parameterList": self.parameterList
        }

    def __str__(self):
        return f"TwoParametersRequest(protocolNumber={self.__protocolNumber}, parameterList={self.parameterList})"