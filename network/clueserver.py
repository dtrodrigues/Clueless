import random
from collections import deque
from twisted.python import log
from twisted.internet import protocol
from twisted.application import service

from messageprotocol import MessageReceiver

cluePlayers = ['Scarlett',
               'Mustard',
               'White',
               'Green',
               'Peacock',
               'Plum']
               
class GameServerProtocol(MessageReceiver):

    def __init__(self):
        self.playerName = None
        self.players = None

    def connectionMade(self):
        peer = self.transport.getPeer()
        log.msg("Connection made from {0}:{1}".format(peer.host, peer.port))

        self.factory.findOpponents(self)

    def connectionLost(self, reason):
        peer = self.transport.getPeer()
        log.msg("Connection lost from {0}:{1}".format(peer.host, peer.port))
        self.factory.playerDisconnected(self)

    def assignPlayer(self, assignedName):
        self.playerName = assignedName
        
    def startGame(self, playerMap):
        self.players = playerMap
        
    def messageReceived(self, message):
        """Called whenever a message is received from a client"""
        peer = self.transport.getPeer()
        log.msg('Message received from {0}:{1}:{2}'.format(self.playerName, 
                                                           peer.host, 
                                                           peer.port))
        for character in self.players:
            if character != self.playerName:
                self.players[character].sendMessage(message)


class GameFactory(protocol.ServerFactory):

    protocol = GameServerProtocol


    def __init__(self, service):
        self.service = service
        self.availablePlayers = cluePlayers
        self.assignedPlayers = {}
        
    def findOpponents(self, player):
    
        assignedPlayer = self.availablePlayers.pop()
        peer = player.transport.getPeer()
        log.msg('{0}:{1} assigned to {2}'.format(peer.host, peer.port, 
                                                 assignedPlayer))
        self.assignedPlayers[assignedPlayer] = player
        player.assignPlayer(assignedPlayer)
        
        #wait for other players
            
        if self.availablePlayers == []:
            #six players joined so start game
            log.msg('Six players joined, starting game')
            for player in self.assignedPlayers.values():
                player.startGame(self.assignedPlayers)
            
            #reset
            self.assignedPlayers = {}
            self.availablePlayers = cluePlayers
            
            #game started

            
    def playerDisconnected(self, player):
        try:
            self.queue.remove(player)
        except ValueError:
            pass

class GameService(service.Service):
    pass

