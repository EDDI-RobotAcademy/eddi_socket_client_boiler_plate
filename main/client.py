import colorama

from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from command_analyzer.service.command_analyzer_service_impl import CommandAnalyzerServiceImpl
from command_executor.service.command_executor_service_impl import CommandExecutorServiceImpl
from initializer.init_domain import DomainInitializer
from os_detector.detect import OperatingSystemDetector
from os_detector.operating_system import OperatingSystem
from receiver.service.receiver_service_impl import ReceiverServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
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
    clientSocketService.connectToTargetHostUnitlSuccess()

    transmitterService = TransmitterServiceImpl.getInstance()
    transmitterService.requestToInjectClientSocket(clientSocket)

    receiverService = ReceiverServiceImpl.getInstance()
    receiverService.requestToInjectClientSocket(clientSocket)

    commandAnalyzerService = CommandAnalyzerServiceImpl.getInstance()
    commandExecutorService = CommandExecutorServiceImpl.getInstance()

    taskWorkerService = TaskWorkerServiceImpl.getInstance()
    taskWorkerService.createTaskWorker("Receiver", receiverService.requestToReceiveCommand)
    taskWorkerService.executeTaskWorker("Receiver")

    taskWorkerService.createTaskWorker("CommandAnalyzer", commandAnalyzerService.analysisCommand)
    taskWorkerService.executeTaskWorker("CommandAnalyzer")

    taskWorkerService.createTaskWorker("CommandExecutor", commandExecutorService.executeCommand)
    taskWorkerService.executeTaskWorker("CommandExecutor")

    taskWorkerService.createTaskWorker("Transmitter", transmitterService.requestToTransmitResult)
    taskWorkerService.executeTaskWorker("Transmitter")
