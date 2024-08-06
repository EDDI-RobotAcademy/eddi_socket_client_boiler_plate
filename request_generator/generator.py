import json

from request_generator.request_class_map import RequestClassMap


class RequestGenerator:
    @staticmethod
    def generate(decodedData):
        print("RequestGenerator: generate()")
        dataDict = json.loads(decodedData)

        for requestTypeName in RequestClassMap.requestClassMap:
            if requestTypeName in dataDict:
                requestData = dataDict[requestTypeName]
                requestClass = RequestClassMap.getRequestClass(requestTypeName)
                if not requestData:
                    return requestClass()
                else:
                    return requestClass(**requestData)

        raise ValueError("서포트하지 않는 Request Type 입니다!")
