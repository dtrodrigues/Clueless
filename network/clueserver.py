from twisted.python import log
from twisted.internet import protocol
from twisted.protocols import basic
from twisted.application import service
import server

class GameServerProtocol(basic.LineReceiver):

    def __init__(self):
        #game = server.Server()
        self.players = None

    def connectionMade(self):
        peer = self.transport.getPeer()
        log.msg("Connection made from {0}:{1}".format(peer.host, peer.port))

        self.factory.findOpponents(self)

    def connectionLost(self, reason):
        peer = self.transport.getPeer()
        log.msg("Connection lost from {0}:{1}".format(peer.host, peer.port))
        self.factory.playerDisconnected(self)
        
    def setPlayers(self, assignedPlayers):
        self.players = assignedPlayers
        
    def lineReceived(self, line):
        """Called whenever a message is received from a client"""
        peer = self.transport.getPeer()
        log.msg('Message received from {0}:{1}'.format(peer.host, 
                                                           peer.port))
        #for player in self.players:
        #    player.sendMessage(message)
        print line    
        response = self.factory.game.invoke(line)
        print response
        for player in self.players:
            player.sendLine(response)

            
class GameFactory(protocol.ServerFactory):

    protocol = GameServerProtocol


    def __init__(self, service):
        self.service = service
        self.availablePlayers = 6
        self.assignedPlayers = []
        
        self.game = server.Server()
        
        
    def findOpponents(self, player):
    
        if self.availablePlayers == 0:
            log.msg('{0}:{1} tried to join the game but there is no room'.format(peer.host, peer.port))
            return
        else:
            self.availablePlayers -= 1
            peer = player.transport.getPeer()
            log.msg('{0}:{1} assigned to game'.format(peer.host, peer.port))
            self.assignedPlayers.append(player)
            
            for player in self.assignedPlayers:
                player.setPlayers(self.assignedPlayers)
            
    def playerDisconnected(self, player):
        pass

class GameService(service.Service):
    pass

