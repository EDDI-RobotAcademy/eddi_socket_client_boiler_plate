from dice.service.request.list_dice_request import ListDiceRequest
from dice.service.request.roll_dice_request import RollDiceRequest
from parameter_test.service.request.n_parameter_request import NParametersRequest
from parameter_test.service.request.n_parameters_gathering_output_request import NParametersGatheringOutputRequest
from parameter_test.service.request.one_parameter_request import OneParametersRequest
from parameter_test.service.request.two_parameter_request import TwoParametersRequest
from utility.color_print import ColorPrinter

from .request_type import RequestType


class RequestClassMap:
    # TODO: 싱글톤 구성을 하지 않아 여러 개가 만들어져 외부에서 사용 할 때 정보 주입이 제대로 안됨
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.requestClassMap = {
                RequestType.ROLL_DICE.name: RollDiceRequest,
                RequestType.LIST_DICE.name: ListDiceRequest,

                RequestType.ONE_PARAMETERS.name: OneParametersRequest,
                RequestType.TWO_PARAMETERS.name: TwoParametersRequest,
                RequestType.N_PARAMETERS.name: NParametersRequest,

                RequestType.N_PARAMETERS_GATHERING_OUTPUT.name: NParametersGatheringOutputRequest,
            }

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getRequestClass(self, requestTypeName):
        return self.requestClassMap.get(requestTypeName)

    def addRequestClass(self, requestTypeName, requestClass):
        self.requestClassMap[requestTypeName] = requestClass

    def printRequestClassMap(self, ):
        ColorPrinter.print_important_data("RequestClassMap", self.requestClassMap)
