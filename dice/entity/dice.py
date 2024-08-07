import random


class Dice:
    MIN = 1
    MAX = 6

    __number = None

    def __init__(self):
        self.__number = random.randint(self.MIN, self.MAX)

    def getNumber(self):
        return self.__number

    def __str__(self):
        return f"number: {self.__number}"
