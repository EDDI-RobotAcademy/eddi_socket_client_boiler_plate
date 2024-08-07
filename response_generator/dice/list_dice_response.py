from request_generator.base_request import BaseResponse
from response_generator.response_type import ResponseType


class ListDiceResponse(BaseResponse):
    def __init__(self, diceList):
        self.protocolNumber = ResponseType.LIST_DICE.value
        self.diceList = diceList

    def toDictionary(self):
        return {
            "protocolNumber": self.protocolNumber,
            "diceList": [str(dice) for dice in self.diceList]
        }

    def __str__(self):
        diceListString = ", ".join([str(dice) for dice in self.diceList])
        return f"ListDiceRequest(protocolNumber={self.protocolNumber}, diceList=[{diceListString}])"