from response_generator.response_type import ResponseType
from utility.color_print import ColorPrinter


class NParametersGatheringOutputResponse:
    def __init__(self, responseData):
        self.protocolNumber = ResponseType.N_PARAMETERS_GATHERING_OUTPUT.value

        for key, value in responseData.items():
            setattr(self, key, value)

    @classmethod
    def fromResponse(cls, responseData):
        ColorPrinter.print_important_data("responseData", responseData)
        return cls(responseData)

    def toDictionary(self):
        return self.__dict__

    def __str__(self):
        return f"NParametersGatheringOutputResponse({self.__dict__})"