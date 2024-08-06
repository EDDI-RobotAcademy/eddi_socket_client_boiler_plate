from enum import Enum


class CustomProtocolNumber(Enum):
    ROLL_DICE = 1
    LIST_DICE = 2

    @classmethod
    def hasValue(cls, value):
        return any(value == item.value for item in cls)
