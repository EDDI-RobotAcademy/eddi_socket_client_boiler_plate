import time

import colorama

from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from command_analyzer.service.command_analyzer_service_impl import CommandAnalyzerServiceImpl
from command_executor.service.command_executor_service_impl import CommandExecutorServiceImpl
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

if __name__ == "__main__":
    colorama.init(autoreset=True)

    detectedOperatingSystem = OperatingSystemDetector.checkCurrentOperatingSystem()
    ColorPrinter.print_important_data("detectedOperatingSystem", detectedOperatingSystem)

    if detectedOperatingSystem is OperatingSystem.UNKNOWN:
        ColorPrinter.print_important_message("범용 운영체제 외에는 실행 할 수 없습니다!")
        exit(1)

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

    # threadWorkerService = ThreadWorkerServiceImpl.getInstance(8)
    # threadWorkerService.createThreadWorker("Receiver", receiverService.requestToReceiveCommand)
    # threadWorkerService.executeThreadWorker("Receiver")
    #
    # threadWorkerService.createThreadWorker("CommandAnalyzer", commandAnalyzerService.analysisCommand)
    # threadWorkerService.executeThreadWorker("CommandAnalyzer")
    #
    # threadWorkerService.createThreadWorker("CommandExecutor", commandExecutorService.executeCommand)
    # threadWorkerService.executeThreadWorker("CommandExecutor")
    #
    # threadWorkerService.createThreadWorker("Transmitter", transmitterService.requestToTransmitResult)
    # threadWorkerService.executeThreadWorker("Transmitter")

    threadWorkerPoolService = ThreadWorkerPoolServiceImpl.getInstance()
    threadWorkerPoolService.createThreadWorkerPool("Receiver", 6)
    threadWorkerPoolService.allocateExecuteFunction("Receiver", receiverService.requestToReceiveCommand)
    receiverFutures = threadWorkerPoolService.executeThreadPoolWorker("Receiver")

    threadWorkerPoolService.createThreadWorkerPool("CommandAnalyzer", 6)
    threadWorkerPoolService.allocateExecuteFunction("CommandAnalyzer", commandAnalyzerService.analysisCommand)
    threadWorkerPoolService.executeThreadPoolWorker("CommandAnalyzer")

    threadWorkerPoolService.createThreadWorkerPool("CommandExecutor", 5)
    threadWorkerPoolService.allocateExecuteFunction("CommandExecutor", commandExecutorService.executeCommand)
    threadWorkerPoolService.executeThreadPoolWorker("CommandExecutor")

    threadWorkerPoolService.createThreadWorkerPool("Transmitter", 1)
    threadWorkerPoolService.allocateExecuteFunction("Transmitter", transmitterService.requestToTransmitResult)
    threadWorkerPoolService.executeThreadPoolWorker("Transmitter")

    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")