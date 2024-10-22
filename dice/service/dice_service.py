from abc import ABC, abstractmethod


class DiceService(ABC):
    @abstractmethod
    def rollDice(self, ipcExecutorConditionalCustomExecutorChannel):
        pass

    @abstractmethod
    def diceList(self, ipcExecutorConditionalCustomExecutorChannel):
        pass

    @abstractmethod
    async def asyncRollDice(self, ipcExecutorConditionalCustomExecutorChannel):
        pass