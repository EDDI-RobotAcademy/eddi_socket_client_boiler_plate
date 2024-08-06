import json

from response_generator.response_type import ResponseType


class ResponseGenerator:
    @staticmethod
    def generator(decodedData):
        data_dict = json.loads(decodedData)

        for response_type in ResponseType:
            if response_type.name in data_dict:
                response_data = data_dict[response_type.name]
                return response_data

        raise ValueError("서포트하지 않는 Response Type 입니다")
