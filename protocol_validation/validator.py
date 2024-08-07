from custom_protocol.entity.custom_protocol import CustomProtocolNumber


class ProtocolValidator:
    @staticmethod
    def validate(receivedData):
        try:
            protocolNumber = receivedData.getProtocolNumber()

            if not CustomProtocolNumber.hasValue(protocolNumber):
                raise ValueError(f"지원하지 않는 프로토콜 번호입니다: {protocolNumber}")

            return True

        except ValueError as e:
            print(f"유효성 검증 실패: {e}")
            return False
