from custom_protocol.entity.custom_protocol import CustomProtocolNumber


class PacketLengthResponse:
    def __init__(self, packetDataLength):
        self.protocolNumber = CustomProtocolNumber.DATA_LENGTH.value
        self.packetDataLength = packetDataLength

    def getPacketDataLength(self):
        return self.packetDataLength

    def toDictionary(self):
        return {
            "protocolNumber": self.protocolNumber,
            "packetDataLength": self.packetDataLength
        }

    def __str__(self):
        return f"PacketLengthResponse(protocolNumber={self.protocolNumber}, packetDataLength={self.packetDataLength})"
