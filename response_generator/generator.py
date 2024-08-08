from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from response_generator.dice.list_dice_response import ListDiceResponse
from response_generator.response_class_map import ResponseClassMap


class ResponseGenerator:
    @staticmethod
    def generate(protocol, data=None):
        protocolEnum = CustomProtocolNumber(protocol)
        responseClass = ResponseClassMap.getResponseClass(protocolEnum.name)
        if responseClass:
            if data:
                diceNumberList = data.getDiceNumberList()
                return responseClass(diceNumberList)
            else:
                return responseClass()

        raise ValueError("서포트하지 않는 Response Type 입니다")
