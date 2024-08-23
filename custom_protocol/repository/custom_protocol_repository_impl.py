import asyncio
import concurrent
import json
import os
import subprocess
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
                OperatingSystem.LINUX: cls.__instance.macosThreadExecutionFunction,
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

    def execute_in_thread(self, userDefinedFunction, parameterList, result_queue):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.__executeAsyncFunction(userDefinedFunction, parameterList))
            result_queue.put(result)
        except Exception as e:
            result_queue.put(e)
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    # TODO: 추후 개선이 필요하겠지만 지금은 그냥 Rust 코드로 구동하자 (Mac OS 전용)
    # async def macosThreadExecutionFunction(self, userDefinedFunction, parameterList):
    #     def threadFunction(loop, resultQueue):
    #         asyncio.set_event_loop(loop)
    #
    #         try:
    #             serviceInstance = userDefinedFunction.__self__
    #
    #             if hasattr(serviceInstance, userDefinedFunction.__name__):
    #                 result = loop.run_until_complete(getattr(serviceInstance, userDefinedFunction.__name__)(*parameterList))
    #             else:
    #                 raise ValueError("함수 구성이 잘못되었음!")
    #
    #             resultQueue.put(result)
    #         except Exception as e:
    #             resultQueue.put(e)
    #         finally:
    #             loop.run_until_complete(loop.shutdown_asyncgens())
    #             loop.close()
    #
    #     resultQueue = Queue()
    #     loop = asyncio.new_event_loop()
    #
    #     thread = threading.Thread(target=threadFunction, args=(loop, resultQueue))
    #     thread.start()
    #     thread.join()
    #
    #     result = resultQueue.get()
    #     ColorPrinter.print_important_data("macosThreadExecutionFunction result", result)
    #     if isinstance(result, Exception):
    #         raise result
    #
    #     return result

    def macosThreadExecutionFunction(self, userDefinedFunction, parameterList):
        # Mac OS에서 Project Top으로 잡힘
        currentWorkDirectory = os.getcwd()

        rustBinaryRelativePath = "task_executor/target/release/task_executor"
        rustBinaryAbsolutePath = os.path.join(currentWorkDirectory, rustBinaryRelativePath)

        fullPackagePath = userDefinedFunction.__module__
        basePackagePath = fullPackagePath.split(".")[0]
        className = userDefinedFunction.__class__.__name__
        userDefinedFunctionName = userDefinedFunction.__name__

        result = None

        try:
            result = subprocess.run([
                rustBinaryAbsolutePath,
                fullPackagePath,
                basePackagePath,
                className,
                userDefinedFunctionName,
                json.dumps(parameterList)
            ], capture_output=True, text=True)
            ColorPrinter.print_important_data("Rust Task Executor 구동 결과", result)
        except Exception as e:
            ColorPrinter.print_important_data("바이너리 구동에 실패! (바이너리를 생성하세요)", str(e))

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
    