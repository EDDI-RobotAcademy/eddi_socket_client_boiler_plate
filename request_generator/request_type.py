from enum import Enum

class RequestType(Enum):
    ROLL_DICE = 1
    LIST_DICE = 2

    ONE_PARAMETERS = 11
    TWO_PARAMETERS = 12
    N_PARAMETERS = 13

    N_PARAMETERS_GATHERING_OUTPUT = 21
