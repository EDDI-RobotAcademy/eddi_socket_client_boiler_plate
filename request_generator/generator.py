import json

from request_generator.request_class_map import RequestClassMap


class RequestGenerator:
    @staticmethod
    def generate(protocol, data):
        print("RequestGenerator: generate()")
        requestClass = RequestClassMap.getRequestClass(protocol.name)
        if requestClass:
            if data:
                return requestClass(**data)
            else:
                return requestClass()

        raise ValueError("서포트하지 않는 Request Type 입니다!")
