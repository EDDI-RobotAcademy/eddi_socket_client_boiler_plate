from os_detector.operating_system import OperatingSystem


class OperatingSystemMap:
    osMap = {
        "Windows": OperatingSystem.WINDOWS,
        "Linux": OperatingSystem.LINUX,
        "Darwin": OperatingSystem.MACOS,
    }

    @staticmethod
    def getOperatingSystemMap():
        return OperatingSystemMap.osMap
