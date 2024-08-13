from request_generator.base_request import BaseRequest
from request_generator.request_type import RequestType


class NParametersGatheringOutputRequest(BaseRequest):
    def __init__(self, **kwargs):
        self.__protocolNumber = RequestType.N_PARAMETERS_GATHERING_OUTPUT.value
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
        return f"NParametersGatheringOutputRequest(protocolNumber={self.__protocolNumber}, parameterList={self.parameterList})"