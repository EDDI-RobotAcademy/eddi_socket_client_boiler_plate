from abc import ABC, abstractmethod


class DiceService(ABC):
    @abstractmethod
    def rollDice(self):
        pass

    @abstractmethod
    def diceList(self):
        pass

    @abstractmethod
    async def asyncRollDice(self):
        pass