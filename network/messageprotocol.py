from twisted.protocols import basic
import pickle

class MessageReceiver(basic.LineOnlyReceiver):

    def lineReceived(self, message):
        self.messageReceived(pickle.loads(message))

    def messageReceived(self, message):
        raise NotImplementedError

    def sendMessage(self, message):
        self.sendLine(pickle.dumps(message))

