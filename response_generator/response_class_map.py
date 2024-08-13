from response_generator.dice.list_dice_response import ListDiceResponse
from response_generator.parameter_test.n_parameters_gathering_output_response import NParametersGatheringOutputResponse
from response_generator.response_type import ResponseType


class ResponseClassMap:
    responseClassMap = {
        ResponseType.LIST_DICE.name: ListDiceResponse,

        ResponseType.N_PARAMETERS_GATHERING_OUTPUT.name: NParametersGatheringOutputResponse,
    }

    @staticmethod
    def getResponseClass(responseTypeName):
        return ResponseClassMap.responseClassMap.get(responseTypeName)
