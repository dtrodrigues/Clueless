import random
from collections import deque
from twisted.python import log
from twisted.internet import protocol
from twisted.application import service

from messageprotocol import MessageReceiver
               
class GameServerProtocol(MessageReceiver):

    def __init__(self):
        self.players = None

    def connectionMade(self):
        peer = self.transport.getPeer()
        log.msg("Connection made from {0}:{1}".format(peer.host, peer.port))

        self.factory.findOpponents(self)

    def connectionLost(self, reason):
        peer = self.transport.getPeer()
        log.msg("Connection lost from {0}:{1}".format(peer.host, peer.port))
        self.factory.playerDisconnected(self)
        
    def startGame(self, assignedPlayers):
        self.players = assignedPlayers
        
    def messageReceived(self, message):
        """Called whenever a message is received from a client"""
        peer = self.transport.getPeer()
        log.msg('Message received from {0}:{1}'.format(peer.host, 
                                                           peer.port))
        for player in self.players:
            player.sendMessage(message)


class GameFactory(protocol.ServerFactory):

    protocol = GameServerProtocol


    def __init__(self, service):
        self.service = service
        self.availablePlayers = 6
        self.assignedPlayers = []
        
    def findOpponents(self, player):
        
        self.availablePlayers -= 1
        
        peer = player.transport.getPeer()
        log.msg('{0}:{1} assigned to game'.format(peer.host, peer.port))
        self.assignedPlayers.append(player)
        
        #wait for other players
            
        if self.availablePlayers == 0:
            #six players joined so start game
            log.msg('Six players joined, starting game')
            for player in self.assignedPlayers:
                player.startGame(self.assignedPlayers)
            
            #reset
            self.assignedPlayers = []
            self.availablePlayers = 6
            
            #game started

            
    def playerDisconnected(self, player):
        
        pass

class GameService(service.Service):
    pass

