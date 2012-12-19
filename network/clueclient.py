#!/usr/bin/env python
import optparse
from twisted.protocols import basic
from twisted.internet import protocol
from twisted.internet.task import LoopingCall

from view.client import Client
#from view.clueGui import ClueGUI
from view.gamerunner import ClueGui

class GameClientProtocol(basic.LineReceiver):

    def __init__(self):
        self.playerName = None
        self.debug_enabled = False


    def out(self, *messages):
        for message in messages:
            print message

    def debug(self, *messages):
        if self.debug_enabled:
            self.out(*messages)

    def connectionMade(self):
        self.factory.client.set_connection(self)
        self.factory.client.run()
        #self.out("Connected!")

    def lineReceived(self, line):
        #self.out("Message received from server: %s" % message)
        self.factory.client.handle_action(line)

class GameClientFactory(protocol.ClientFactory):
    protocol = GameClientProtocol

    def startedConnecting(self, connector):
        destination = connector.getDestination()
        print "Connecting to server {0}:{1}, please wait...".format(destination.host, destination.port)

    def clientConnectionFailed(self, connector, reason):
        print reason.getErrorMessage()
        from twisted.internet import reactor
        reactor.stop()  #@UndefinedVariable

    def clientConnectionLost(self, connector, reason):
        print reason.getErrorMessage()
        from twisted.internet import reactor, error
        try:
            reactor.stop()  #@UndefinedVariable
        except error.ReactorNotRunning:
            pass

def parse_args():
    usage = "usage: %prog [options] [[hostname:]port]"

    parser = optparse.OptionParser(usage)

    _, args = parser.parse_args()

    if not args:
        address = "127.0.0.1:20000"
    else:
        address = args[0]

    if ':' not in address:
        host, port = '127.0.0.1', address
    else:
        host, port = address.split(':', 1)

    if not port.isdigit():
        parser.error("Ports must be integers.")

    return host, int(port)


def run_client():
    from twisted.internet import reactor
    host, port = parse_args()
    factory = GameClientFactory()
#   clueGui = ClueGUI()
    clueGui = ClueGui()
    startGame, plyr, char = clueGui.initiate_game()
#   startGame = clueGui.app.startValue
#   plyr = clueGui.app.playerName
#   char = clueGui.app.char
    client = Client(plyr, char, startGame)
    factory.client = client
    clueGui.client = client
    reactor.connectTCP(host, port, factory)  #@UndefinedVariable

    
    lc = LoopingCall(clueGui.one_lap)
    lc.start(.5)
    
    reactor.run()  #@UndefinedVariable

if __name__ == '__main__':
    run_client()

