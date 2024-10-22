from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from dice.repository.dice_repository_impl import DiceRepositoryImpl
from dice.service.dice_service import DiceService
from dice.service.response.list_dice_response import ListDiceResponse


class DiceServiceImpl(DiceService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__diceRepository = DiceRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def rollDice(self, ipcExecutorConditionalCustomExecutorChannel):
        self.__diceRepository.roll()

    def diceList(self, ipcExecutorConditionalCustomExecutorChannel):
        diceList = self.__diceRepository.list()
        return ListDiceResponse(CustomProtocolNumber.LIST_DICE, diceList)

    async def asyncRollDice(self, ipcExecutorConditionalCustomExecutorChannel):
        await self.__diceRepository.asyncRoll()

