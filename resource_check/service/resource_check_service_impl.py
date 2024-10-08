from resource_check.repository.resource_check_repository_impl import ResourceCheckRepositoryImpl
from resource_check.service.resource_check_service import ResourceCheckService


class ResourceCheckServiceImpl(ResourceCheckService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__resourceCheckRepository = ResourceCheckRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def checkMemoryResource(self):
        memoryInfo = self.__resourceCheckRepository.parseMemoryInfo()

        totalMemoryKB = memoryInfo.get('MemTotal', 0)
        availableMemoryKB = memoryInfo.get('MemAvailable', 0)

        totalMemoryGB = totalMemoryKB / (1024 ** 2)
        availableMemoryGB = availableMemoryKB / (1024 ** 2)

        print(f"Total Memory: {totalMemoryGB:.2f} GB")
        print(f"Available Memory: {availableMemoryGB:.2f} GB")
    