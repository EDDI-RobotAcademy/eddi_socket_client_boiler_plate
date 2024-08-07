from response_generator.dice.list_dice_response import ListDiceResponse
from response_generator.dice.roll_dice_response import RollDiceResponse
from response_generator.response_type import ResponseType


class ResponseClassMap:
    responseClassMap = {
        ResponseType.ROLL_DICE.name: RollDiceResponse,
        ResponseType.LIST_DICE.name: ListDiceResponse,
    }

    @staticmethod
    def getResponseClass(responseTypeName):
        return ResponseClassMap.responseClassMap.get(responseTypeName)
