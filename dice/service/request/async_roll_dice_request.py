from request_generator.base_request import BaseRequest
from request_generator.request_type import RequestType


class AsyncRollDiceRequest(BaseRequest):
    def __init__(self):
        self.__protocolNumber = RequestType.ASYNC_ROLL_DICE.value

    def getProtocolNumber(self):
        return self.__protocolNumber

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber
        }

    def __str__(self):
        return f"AsyncRollDiceRequest(protocolNumber={self.__protocolNumber})"
