from request_generator.base_request import BaseRequest
from request_generator.request_type import RequestType


class NParametersRequest(BaseRequest):
    def __init__(self):
        self.__protocolNumber = RequestType.N_PARAMETERS.value

    def getProtocolNumber(self):
        return self.__protocolNumber

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber
        }

    def __str__(self):
        return f"NParametersRequest(protocolNumber={self.__protocolNumber})"