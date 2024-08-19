from abc import ABC, abstractmethod


class DiceRepository(ABC):
    @abstractmethod
    def roll(self):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    async def asyncRoll(self):
        pass
