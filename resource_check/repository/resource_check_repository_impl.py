from resource_check.repository.resource_check_repository import ResourceCheckRepository


class ResourceCheckRepositoryImpl(ResourceCheckRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def parseMemoryInfo(self):
        meminfo = {}

        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split()
                key = parts[0].rstrip(':')
                value = int(parts[1])
                meminfo[key] = value

        return meminfo
