from twisted.protocols import basic

class MessageReceiver(basic.LineOnlyReceiver):

    def lineReceived(self, line):
        self.messageReceived(line)

    def messageReceived(self, line):
        raise NotImplementedError

    def sendMessage(self, line):
        self.sendLine(line)

