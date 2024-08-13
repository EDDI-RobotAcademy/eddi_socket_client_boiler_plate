from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from command_analyzer.service.command_analyzer_service_impl import CommandAnalyzerServiceImpl
from command_executor.service.command_executor_service_impl import CommandExecutorServiceImpl
from custom_protocol.entity.custom_protocol import CustomProtocolNumber
from custom_protocol.service.custom_protocol_service_impl import CustomProtocolServiceImpl
from dice.service.dice_service_impl import DiceServiceImpl
from ipc_queue.repository.ipc_queue_repository_impl import IPCQueueRepositoryImpl
from ipc_queue.service.ipc_queue_service_impl import IPCQueueServiceImpl
from parameter_test.service.parameter_test_service_impl import ParameterTestServiceImpl
from receiver.service.receiver_service_impl import ReceiverServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from thread_worker.service.thread_worker_service_impl import ThreadWorkerServiceImpl
from transmitter.service.transmitter_service_impl import TransmitterServiceImpl


class DomainInitializer:
    @staticmethod
    def initThreadWorkerDomain():
        ThreadWorkerServiceImpl.getInstance()

    @staticmethod
    def initTaskWorkerDomain():
        TaskWorkerServiceImpl.getInstance()

    @staticmethod
    def initIPCQueueDomain():
        ipcQueueService = IPCQueueServiceImpl.getInstance()
        ipcQueueService.createEssentialIPCQueue()

    @staticmethod
    def initDiceDomain():
        DiceServiceImpl.getInstance()

    @staticmethod
    def initCustomProtocolDomain():
        customProtocolService = CustomProtocolServiceImpl.getInstance()
        diceService = DiceServiceImpl.getInstance()
        parameterTestService = ParameterTestServiceImpl.getInstance()

        # 디폴트 프로토콜 등록을 여기서 했음
        customProtocolService.registerCustomProtocol(
            CustomProtocolNumber.ROLL_DICE,
            diceService.rollDice
        )

        customProtocolService.registerCustomProtocol(
            CustomProtocolNumber.LIST_DICE,
            diceService.diceList
        )

        customProtocolService.registerCustomProtocol(
            CustomProtocolNumber.ONE_PARAMETERS,
            parameterTestService.useOneParameters
        )

        customProtocolService.registerCustomProtocol(
            CustomProtocolNumber.TWO_PARAMETERS,
            parameterTestService.useTwoParameters
        )

        customProtocolService.registerCustomProtocol(
            CustomProtocolNumber.N_PARAMETERS,
            parameterTestService.useNParameters
        )

    @staticmethod
    def initClientSocketDomain():
        ClientSocketServiceImpl.getInstance()

    @staticmethod
    def initReceiverDomain():
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcReceiverAnalyzerChannel = ipcQueueRepository.getIPCReceiverAnalyzerChannel()

        receiverService = ReceiverServiceImpl.getInstance()
        receiverService.requestToInjectReceiverAnalyzerChannel(ipcReceiverAnalyzerChannel)

    @staticmethod
    def initCommandAnalyzerDomain():
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcReceiverAnalyzerChannel = ipcQueueRepository.getIPCReceiverAnalyzerChannel()
        ipcAnalyzerExecutorChannel = ipcQueueRepository.getIPCAnalyzerExecutorChannel()

        commandAnalyzerService = CommandAnalyzerServiceImpl.getInstance()
        commandAnalyzerService.requestToInjectReceiverAnalyzerChannel(ipcReceiverAnalyzerChannel)
        commandAnalyzerService.requestToInjectAnalyzerExecutorChannel(ipcAnalyzerExecutorChannel)

    @staticmethod
    def initCommandExecutorDomain():
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcAnalyzerExecutorChannel = ipcQueueRepository.getIPCAnalyzerExecutorChannel()
        ipcExecutorTransmitterChannel = ipcQueueRepository.getIPCExecutorTransmitterChannel()

        commandExecutorService = CommandExecutorServiceImpl.getInstance()
        commandExecutorService.requestToInjectAnalyzerExecutorChannel(ipcAnalyzerExecutorChannel)
        commandExecutorService.requestToInjectExecutorTransmitterChannel(ipcExecutorTransmitterChannel)

    @staticmethod
    def initTransmitterDomain():
        ipcQueueRepository = IPCQueueRepositoryImpl.getInstance()
        ipcExecutorTransmitterChannel = ipcQueueRepository.getIPCExecutorTransmitterChannel()

        transmitterService = TransmitterServiceImpl.getInstance()
        transmitterService.requestToInjectExecutorTransmitterChannel(ipcExecutorTransmitterChannel)

    @staticmethod
    def initEachDomain():
        DomainInitializer.initDiceDomain()
        DomainInitializer.initCustomProtocolDomain()

        DomainInitializer.initThreadWorkerDomain()
        DomainInitializer.initTaskWorkerDomain()

        DomainInitializer.initIPCQueueDomain()

        DomainInitializer.initClientSocketDomain()

        DomainInitializer.initReceiverDomain()
        DomainInitializer.initCommandAnalyzerDomain()
        DomainInitializer.initCommandExecutorDomain()
        DomainInitializer.initTransmitterDomain()


