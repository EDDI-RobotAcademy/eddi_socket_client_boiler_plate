from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from utility.color_print import ColorPrinter

try:
    from user_defined_protocol.protocol import UserDefinedProtocolNumber
except ImportError:
    UserDefinedProtocolNumber = None
    ColorPrinter.print_important_message("UserDefinedProtocolNumber는 사용자가 추가적인 프로토콜을 확장하기 위해 사용합니다.")


class ProtocolValidator:
    @staticmethod
    def validate(receivedData):
        try:
            protocolNumber = receivedData.getProtocolNumber()

            if not (CustomProtocolNumber.hasValue(protocolNumber) or
                    UserDefinedProtocolNumber.hasValue(protocolNumber)):
                raise ValueError(f"지원하지 않는 프로토콜 번호입니다: {protocolNumber}")

            return True

        except ValueError as e:
            print(f"유효성 검증 실패: {e}")
            return False
