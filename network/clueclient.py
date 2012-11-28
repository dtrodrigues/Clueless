#!/usr/bin/env python
import optparse
import re
from twisted.protocols import basic
from twisted.internet import protocol, stdio
from twisted.internet.task import LoopingCall

from view.client import Client
from view.player import ClueGUI

from messageprotocol import MessageReceiver


class UserInputProtocol(basic.LineReceiver):

    from os import linesep as delimiter  #@UnusedImport

    def __init__(self, callback):
        self.callback = callback

    def lineReceived(self, line):
        self.callback(line)

class GameClientProtocol(MessageReceiver):


    def __init__(self):
        #self.game = Game()
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

    def userInputReceived(self, string):
        #create a dummy message from first two words on the command line
        self.sendMessage(string)

    def messageReceived(self, message):
        #self.out("Message received from server: %s" % message)
        self.factory.client.handle_action(message)

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

    a, args = parser.parse_args()
    startGame = False

    if not args:
        address = "127.0.0.1:20000"
    elif len(args) == 2:
        address = args[1]
        startGame = (args[0] == "true")
    else:
        startGame = (args[0] == "true")
        address = "127.0.0.1:20000"

    if ':' not in address:
        host, port = '127.0.0.1', address
    else:
        host, port = address.split(':', 1)

    if not port.isdigit():
        parser.error("Ports must be integers.")

    return startGame, host, int(port)

def run_client():
    from twisted.internet import reactor
    startGame, host, port = parse_args()
    factory = GameClientFactory()
    clueGui = ClueGUI()
    plyr, char = clueGui.initiate_game()
    client = Client(plyr, char, startGame)
    factory.client = client
    clueGui.client = client
    reactor.connectTCP(host, port, factory)  #@UndefinedVariable

    
    lc = LoopingCall(clueGui.one_lap)
    lc.start(.5)
    
    reactor.run()  #@UndefinedVariable

if __name__ == '__main__':
    run_client()

