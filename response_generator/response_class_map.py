from response_generator.dice.list_dice_response import ListDiceResponse
from response_generator.parameter_test.n_parameters_gathering_output_response import NParametersGatheringOutputResponse
from response_generator.response_type import ResponseType


class ResponseClassMap:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.responseClassMap = {
                ResponseType.LIST_DICE.name: ListDiceResponse,

                ResponseType.N_PARAMETERS_GATHERING_OUTPUT.name: NParametersGatheringOutputResponse,
            }

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getResponseClass(self, responseTypeName):
        return self.responseClassMap.get(responseTypeName)

    def addResponseClass(self, responseTypeName, responseClass):
        self.responseClassMap[responseTypeName.name] = responseClass
