from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from transmitter.service.transmitter_service_impl import TransmitterServiceImpl


class DomainInitializer:

    @staticmethod
    def initClientSocketDomain():
        ClientSocketServiceImpl.getInstance()

    @staticmethod
    def initTransmitterDomain():
        transmitterService = TransmitterServiceImpl.getInstance()

    @staticmethod
    def initEachDomain():
        DomainInitializer.initClientSocketDomain()
        DomainInitializer.initTransmitterDomain()

