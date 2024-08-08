class ListDiceResponse:
    def __init__(self, protocolNumber, diceList):
        self.protocolNumber = protocolNumber
        self.diceList = diceList

    def toDictionary(self):
        return {
            "protocolNumber": self.protocolNumber,
            "diceList": self.diceList
        }

    def __str__(self):
        return f"ListDiceResponse(protocolNumber={self.protocolNumber}, diceList={self.diceList})"
