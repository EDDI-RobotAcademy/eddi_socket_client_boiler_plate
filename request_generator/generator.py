import json

from request_generator.request_class_map import RequestClassMap


class RequestGenerator:
    __instance = None
    __requestClassMapInstance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestToInjectUserDefinedRequestClassMapInstance(self, requestClassMapInstance):
        self.__requestClassMapInstance = requestClassMapInstance

    def generate(self, protocol, data):
        requestClass = self.__requestClassMapInstance.getRequestClass(protocol.name)
        if requestClass:
            if data:
                return requestClass(data=data)
            else:
                return requestClass()

        raise ValueError("서포트하지 않는 Request Type 입니다!")
