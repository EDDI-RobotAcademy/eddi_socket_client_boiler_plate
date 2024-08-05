import colorama

from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl

if __name__ == "__main__":
    colorama.init(autoreset=True)

    clientSocketService = ClientSocketServiceImpl.getInstance()
    clientSocket = clientSocketService.createClientSocket()
    clientSocketService.connectToTargetHostUnitlSuccess()

