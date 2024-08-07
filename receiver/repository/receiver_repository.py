from abc import ABC, abstractmethod


class ReceiverRepository(ABC):
    @abstractmethod
    def injectClientSocket(self, clientSocket):
        pass

    @abstractmethod
    def injectReceiverAnalyzerChannel(self, ipcReceiverAnalyzerChannel):
        pass

    @abstractmethod
    def sendDataToCommandAnalyzer(self, decodedData):
        pass

    @abstractmethod
    def receive(self):
        pass

    @abstractmethod
    def closeConnection(self):
        pass
