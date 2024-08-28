from enum import Enum


class CustomProtocolNumber(Enum):
    ROLL_DICE = 1
    LIST_DICE = 2

    ASYNC_ROLL_DICE = 4

    ONE_PARAMETERS = 11
    TWO_PARAMETERS = 12
    N_PARAMETERS = 13

    N_PARAMETERS_GATHERING_OUTPUT = 21

    DATA_LENGTH = 7777

    @classmethod
    def hasValue(cls, value):
        return any(value == item.value for item in cls)
