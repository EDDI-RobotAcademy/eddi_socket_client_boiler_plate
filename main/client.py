import threading
import time

import colorama
from functools import partial

from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from command_analyzer.service.command_analyzer_service_impl import CommandAnalyzerServiceImpl
from command_executor.service.command_executor_service_impl import CommandExecutorServiceImpl
from conditional_custom_executor.service.conditional_custom_executor_service_impl import \
    ConditionalCustomExecutorServiceImpl
from initializer.init_domain import DomainInitializer
from os_detector.detect import OperatingSystemDetector
from os_detector.operating_system import OperatingSystem
from receiver.service.receiver_service_impl import ReceiverServiceImpl
from request_generator.request_class_map import RequestClassMap
from response_generator.response_class_map import ResponseClassMap
from ssl_tls.ssl_tls_context_manager import SslTlsContextManager
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from thread_worker.service.thread_worker_service_impl import ThreadWorkerServiceImpl
from thread_worker_pool.service.thread_worker_pool_service_impl import ThreadWorkerPoolServiceImpl
from transmitter.service.transmitter_service_impl import TransmitterServiceImpl
from utility.color_print import ColorPrinter

DomainInitializer.initEachDomain()

stop_event = threading.Event()

if __name__ == "__main__":
    colorama.init(autoreset=True)

    detectedOperatingSystem = OperatingSystemDetector.checkCurrentOperatingSystem()
    ColorPrinter.print_important_data("detectedOperatingSystem", detectedOperatingSystem)

    if detectedOperatingSystem is OperatingSystem.UNKNOWN:
        ColorPrinter.print_important_message("범용 운영체제 외에는 실행 할 수 없습니다!")
        exit(1)

    try:
        clientSocketService = ClientSocketServiceImpl.getInstance()
        clientSocket = clientSocketService.createClientSocket()
        clientSocketService.connectToTargetHostUnitSuccess()

        requestClassMapInstance = RequestClassMap.getInstance()
        responseClassMapInstance = ResponseClassMap.getInstance()

        transmitterService = TransmitterServiceImpl.getInstance()
        transmitterService.requestToInjectUserDefinedResponseClassMapInstance(responseClassMapInstance)

        receiverService = ReceiverServiceImpl.getInstance()
        receiverService.requestToInjectUserDefinedRequestClassMapInstance(requestClassMapInstance)

        commandAnalyzerService = CommandAnalyzerServiceImpl.getInstance()
        commandExecutorService = CommandExecutorServiceImpl.getInstance()

        conditionalCustomExecutorService = ConditionalCustomExecutorServiceImpl.getInstance()

        threadWorkerPoolService = ThreadWorkerPoolServiceImpl.getInstance()

        for receiverId in range(6):
            threadWorkerPoolService.executeThreadPoolWorker(
                f"Receiver-{receiverId}",
                partial(receiverService.requestToReceiveCommand, receiverId)
            )

            # Command Analyzer Thread Pool (6개)
        for analyzerId in range(6):
            threadWorkerPoolService.executeThreadPoolWorker(
                f"CommandAnalyzer-{analyzerId}",
                partial(commandAnalyzerService.analysisCommand, analyzerId)
            )

            # Command Executor Thread Pool (5개)
        for executorId in range(5):
            threadWorkerPoolService.executeThreadPoolWorker(
                f"CommandExecutor-{executorId}",
                partial(commandExecutorService.executeCommand, executorId)
            )

        for conditionalCustomExecutorId in range(5):
            threadWorkerPoolService.executeThreadPoolWorker(
                f"ConditionalCustomExecutor-{conditionalCustomExecutorId}",
                partial(conditionalCustomExecutorService.executeConditionalCustomCommand, conditionalCustomExecutorId)
            )

            # Transmitter Thread Pool (1개)
        threadWorkerPoolService.executeThreadPoolWorker(
            "Transmitter-0",
            partial(transmitterService.requestToTransmitResult, 0)  # 단일 ID 사용
        )

        # 프로그램 종료를 위한 이벤트 대기
        while not stop_event.is_set():
            threading.Event().wait(1)  # 1초 대기

    except Exception as e:
        ColorPrinter.print_important_message(f"An error occurred: {e}")

    finally:
        threadWorkerPoolService.shutdownAll()
