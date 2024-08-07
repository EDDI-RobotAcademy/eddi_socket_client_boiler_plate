class BaseResponse:
    def toDictionary(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
