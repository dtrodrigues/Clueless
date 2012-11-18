#!/usr/bin/env python
import optparse
import re
from functools import partial
from twisted.protocols import basic
from twisted.internet import protocol, stdio
from twisted.internet.task import LoopingCall
import player

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
        stdio.StandardIO(UserInputProtocol(self.userInputReceived))
        self.out("Connected!")

    def userInputReceived(self, string):
        #create a dummy message from first two words on the command line
        self.sendMessage(string)

    def messageReceived(self, message):
        self.out("Message received from server: %s" % message)

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
    reactor.connectTCP(host, port, factory)  #@UndefinedVariable
    #lc = LoopingCall(player.loopOnce)
    #lc.start(.5)
    
    reactor.run()  #@UndefinedVariable

if __name__ == '__main__':
    run_client()

