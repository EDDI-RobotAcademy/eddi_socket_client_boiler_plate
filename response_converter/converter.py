class ResponseConverter:
    @staticmethod
    def convert(response, responseClass):
        if hasattr(responseClass, 'fromResponse'):
            return responseClass.fromResponse(response)

        raise ValueError(f"요청한 {responseClass} 가 fromResponse()를 구동할 수 없습니다!")
