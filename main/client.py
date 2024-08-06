import colorama

from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from command_analyzer.service.command_analyzer_service_impl import CommandAnalyzerServiceImpl
from command_executor.service.command_executor_service_impl import CommandExecutorServiceImpl
from initializer.init_domain import DomainInitializer
from receiver.service.receiver_service_impl import ReceiverServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from transmitter.service.transmitter_service_impl import TransmitterServiceImpl


DomainInitializer.initEachDomain()

if __name__ == "__main__":
    colorama.init(autoreset=True)

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

    taskWorkerService.createTaskWorker("CommandAnalyzer", commandAnalyzerService.analysisCommand())
    taskWorkerService.executeTaskWorker("CommandAnalyzer")

    taskWorkerService.createTaskWorker("CommandExecutor", commandExecutorService.execute_command())
    taskWorkerService.executeTaskWorker("CommandExecutor")

    taskWorkerService.createTaskWorker("Transmitter", transmitterService.requestToTransmitResult)
    taskWorkerService.executeTaskWorker("Transmitter")
