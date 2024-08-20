import asyncio
import concurrent
import threading
from queue import Queue

from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from custom_protocol.repository.custom_protocol_repository import CustomProtocolRepository
from os_detector.detect import OperatingSystemDetector
from os_detector.operating_system import OperatingSystem
from utility.color_print import ColorPrinter

try:
    from user_defined_protocol.protocol import UserDefinedProtocolNumber
except ImportError:
    UserDefinedProtocolNumber = None
    ColorPrinter.print_important_message("UserDefinedProtocolNumber는 사용자가 추가적인 프로토콜을 확장하기 위해 사용합니다.")


class CustomProtocolRepositoryImpl(CustomProtocolRepository):
    __instance = None
    __protocolTable = {}

    __osDependentThreadExecutionTable = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__osDependentThreadExecutionTable = {
                OperatingSystem.WINDOWS: cls.__instance.generalThreadExecutionFunction,
                OperatingSystem.LINUX: cls.__instance.generalThreadExecutionFunction,
                OperatingSystem.MACOS: cls.__instance.macosThreadExecutionFunction,
            }

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def register(self, protocolNumber, customFunction):
        print(f"Registering protocolNumber: {protocolNumber}, customFunction: {customFunction}")

        if protocolNumber is None:
            raise ValueError("프로토콜 번호가 None입니다.")
        if not (CustomProtocolNumber.hasValue(protocolNumber.value) or
                (UserDefinedProtocolNumber is not None and UserDefinedProtocolNumber.hasValue(protocolNumber.value))):
            raise ValueError("프로토콜을 등록 시 반드시 CustomProtocolNumber 혹은 UserDefinedProtocolNumber에 정의된 값을 사용하세요")
        if not callable(customFunction):
            raise  ValueError("customFunction은 프로토콜에 대응하는 함수입니다")

        self.__protocolTable[protocolNumber.value] = customFunction

    def __executeSynchronizeFunction(self, userDefinedFunction, parameterList):
        if parameterList:
            return userDefinedFunction(*parameterList)

        return userDefinedFunction()

    def __extractParameterList(self, requestObject):
        if hasattr(requestObject, 'getParameterList') and callable(requestObject.getParameterList):
            parameterList = requestObject.getParameterList()
            ColorPrinter.print_important_data("parameterList", parameterList)
            return parameterList

        return []

    async def __executeAsyncFunction(self, userDefinedFunction, parameterList):
        return await userDefinedFunction(*parameterList)

    def generalThreadExecutionFunction(self, userDefinedFunction, parameterList):
        try:
            loop = asyncio.get_event_loop()

        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            future = asyncio.ensure_future(self.__executeAsyncFunction(userDefinedFunction, parameterList))
            result = asyncio.get_event_loop().run_until_complete(future)
        else:
            result = loop.run_until_complete(self.__executeAsyncFunction(userDefinedFunction, parameterList))

        return result

    def macosThreadExecutionFunction(self, userDefinedFunction, parameterList):
        def run_in_thread(loop, userDefinedFunction, parameterList, resultQueue):
            asyncio.set_event_loop(loop)
            try:
                future = asyncio.run_coroutine_threadsafe(self.__executeAsyncFunction(userDefinedFunction, parameterList), loop)
                resultQueue.put(future.result())
            except Exception as e:
                resultQueue.put(e)

        loop = asyncio.new_event_loop()
        resultQueue = Queue()

        thread = threading.Thread(target=run_in_thread, args=(loop, userDefinedFunction, parameterList, result_queue))
        thread.start()
        thread.join()

        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

        result = resultQueue.get()
        if isinstance(result, Exception):
            raise result

        return result

    def execute(self, requestObject):
        ColorPrinter.print_important_data("CommandExecutor requestObject -> protocolNumber", requestObject.getProtocolNumber())
        ColorPrinter.print_important_data("customFunction", self.__protocolTable[requestObject.getProtocolNumber()])

        userDefinedFunction = self.__protocolTable[requestObject.getProtocolNumber()]

        parameterList = self.__extractParameterList(requestObject)

        if asyncio.iscoroutinefunction(userDefinedFunction):
            osType = OperatingSystemDetector.checkCurrentOperatingSystem()
            osDependentThreadExecuteFunction = self.__osDependentThreadExecutionTable[osType]
            result = osDependentThreadExecuteFunction(userDefinedFunction, parameterList)
        else:
            result = self.__executeSynchronizeFunction(userDefinedFunction, parameterList)

        ColorPrinter.print_important_data("result", result)

        return result
    