from request_generator.base_request import BaseResponse
from response_generator.response_type import ResponseType


class RollDiceResponse(BaseResponse):
    def __init__(self):
        self.protocolNumber = ResponseType.ROLL_DICE.value

    @classmethod
    def fromResponse(cls, response):
        return None

    def toDictionary(self):
        return {"protocolNumber": self.protocolNumber}

    def __str__(self):
        return f"RollDiceResponse(protocolNumber={self.protocolNumber})"