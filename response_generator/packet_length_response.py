from custom_protocol.entity.custom_protocol import CustomProtocolNumber


class PacketLengthResponse:
    def __init__(self, packetDataLength):
        self.protocolNumber = CustomProtocolNumber.DATA_LENGTH.value
        self.packetDataLength = packetDataLength

    def getPacketDataLength(self):
        return self.packetDataLength

    def toFixedSizeDictionary(self):
        # protocolNumber와 packetDataLength를 고정 크기로 변환
        protocolNumberString = str(self.protocolNumber).ljust(4)
        packetDataLengthString = str(self.packetDataLength).ljust(8)

        return {
            "protocolNumber": protocolNumberString,
            "packetDataLength": packetDataLengthString
        }

    def __str__(self):
        return f"PacketLengthResponse(protocolNumber={self.protocolNumber}, packetDataLength={self.packetDataLength})"
