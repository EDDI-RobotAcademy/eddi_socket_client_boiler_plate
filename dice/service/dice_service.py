from abc import ABC, abstractmethod


class DiceService(ABC):
    @abstractmethod
    def rollDice(self):
        pass
