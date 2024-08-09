import platform

from os_detector.operating_system import OperatingSystem
from os_detector.operating_system_map import OperatingSystemMap
from utility.color_print import ColorPrinter


class OperatingSystemDetector:
    @staticmethod
    def checkCurrentOperatingSystem():
        osName = platform.system()
        ColorPrinter.print_important_data("현재 운영체제", osName)

        osMap = OperatingSystemMap.getOperatingSystemMap()

        return osMap.get(osName, OperatingSystem.UNKNOWN)

