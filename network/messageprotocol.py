from twisted.protocols import basic

class MessageReceiver(basic.LineOnlyReceiver):

    def lineReceived(self, message):
        self.messageReceived(message)

    def messageReceived(self, message):
        raise NotImplementedError

    def sendMessage(self, message):
        self.sendLine(message)

