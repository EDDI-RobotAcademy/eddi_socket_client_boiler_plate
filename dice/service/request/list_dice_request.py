from request_generator.base_request import BaseResponse
from request_generator.request_type import RequestType


class ListDiceRequest(BaseResponse):
    def __init__(self):
        self.__protocolNumber = RequestType.LIST_DICE.value

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber
        }

    def __str__(self):
        return f"ListDiceRequest(protocolNumber={self.__protocolNumber})"
    