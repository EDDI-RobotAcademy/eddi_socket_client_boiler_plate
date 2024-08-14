import json

from request_generator.request_class_map import RequestClassMap


class RequestGenerator:
    @staticmethod
    def generate(protocol, data):
        requestClassMapInstance = RequestClassMap.getInstance()

        requestClass = requestClassMapInstance.getRequestClass(protocol.name)
        if requestClass:
            if data:
                return requestClass(data=data)
            else:
                return requestClass()

        raise ValueError("서포트하지 않는 Request Type 입니다!")
