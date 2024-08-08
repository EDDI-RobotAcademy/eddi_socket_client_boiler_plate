from dice.entity.dice import Dice
from dice.repository.dice_repository import DiceRepository


class DiceRepositoryImpl(DiceRepository):
    __instance = None
    __diceList = []

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def roll(self):
        dice = Dice()
        self.__diceList.append(dice)

    def list(self):
        for dice in self.__diceList:
            print(f"dice: {dice}")

        return self.__diceList
