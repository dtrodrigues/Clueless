from twisted.protocols import basic

class MessageReceiver(basic.LineOnlyReceiver):

    def lineReceived(self, line):
        #line = line.replace("\\n", "\n")
        self.messageReceived(line)

    def messageReceived(self, line):
        raise NotImplementedError

    def sendMessage(self, line):
        self.sendLine(line)

