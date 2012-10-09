import random
from collections import deque
from twisted.python import log
from twisted.internet import protocol
from twisted.application import service

from messageprotocol import MessageReceiver


class GameServerProtocol(MessageReceiver):

    def __init__(self):
        self.game = None
        self.opponent = None

    def connectionMade(self):
        peer = self.transport.getPeer()
        log.msg("Connection made from {0}:{1}".format(peer.host, peer.port))

        # Find an opponent or add self to a queue
        self.factory.findOpponent(self)

    def connectionLost(self, reason):
        peer = self.transport.getPeer()
        log.msg("Connection lost from {0}:{1}".format(peer.host, peer.port))
        self.factory.playerDisconnected(self)

    def messageReceived(self, message):
        """Decodes and runs a command from the received data"""
        log.msg('Data received: {0}'.format(message))
        self.sendMessage(message)


class GameFactory(protocol.ServerFactory):

    protocol = GameServerProtocol
    queue = deque()

    def __init__(self, service):
        self.service = service

    def findOpponents(self, player):
        try:
            opponent = self.queue.popleft()
        except IndexError:
            self.queue.append(player)
        else:
            game = Game()
            player.startGame(game, opponent, side1)
            opponent.startGame(game, player, side2)

    def playerDisconnected(self, player):
        try:
            self.queue.remove(player)
        except ValueError:
            pass

class GameService(service.Service):
    pass

