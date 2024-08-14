from dice.service.request.list_dice_request import ListDiceRequest
from dice.service.request.roll_dice_request import RollDiceRequest
from parameter_test.service.request.n_parameter_request import NParametersRequest
from parameter_test.service.request.n_parameters_gathering_output_request import NParametersGatheringOutputRequest
from parameter_test.service.request.one_parameter_request import OneParametersRequest
from parameter_test.service.request.two_parameter_request import TwoParametersRequest
from utility.color_print import ColorPrinter

from .request_type import RequestType


class RequestClassMap:
    requestClassMap = {
        RequestType.ROLL_DICE.name: RollDiceRequest,
        RequestType.LIST_DICE.name: ListDiceRequest,

        RequestType.ONE_PARAMETERS.name: OneParametersRequest,
        RequestType.TWO_PARAMETERS.name: TwoParametersRequest,
        RequestType.N_PARAMETERS.name: NParametersRequest,

        RequestType.N_PARAMETERS_GATHERING_OUTPUT.name: NParametersGatheringOutputRequest,
    }

    @staticmethod
    def getRequestClass(requestTypeName):
        return RequestClassMap.requestClassMap.get(requestTypeName)

    @staticmethod
    def addRequestClass(requestTypeName, requestClass):
        RequestClassMap.requestClassMap[requestTypeName] = requestClass


    @staticmethod
    def printRequestClassMap():
        ColorPrinter.print_important_data("RequestClassMap", RequestClassMap.requestClassMap)
