import colorama

from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from initializer.init_domain import DomainInitializer
from receiver.service.receiver_service_impl import ReceiverServiceImpl
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