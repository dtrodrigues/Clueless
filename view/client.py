import pickle
import logic.message as m
from view.player import Character
from logic.game import Board


servToGui = {"Study": "study", "Hall": "hall", "Lounge": "lounge", "Library": "library", "Billiard Room": "billiard", "Dining Room": "dining", "Conservatory": "conservatory", "Ballroom": "ballroom", "Kitchen": "kitchen", "Miss Scarlet": "scarlet", "Colonel Mustard": "mustard", "Mrs. White": "white", "Mr. Green": "green", "Mrs. Peacock": "peacock", "Professor Plum": "plum", "Candlestick": "candlestick", "Dagger": "knife", "Lead Pipe": "lead", "Revolver": "revolver", "Rope": "rope", "Wrench": "wrench"}

guiToServ = {val:key for key,val in servToGui.iteritems()}


class Client():
    
    def __init__(self, name, char, startGame):
        self.name = name
        self.char = char
        self.startGame = startGame

    def set_connection(self, connection):
        self.connection = connection

    def run(self):
        self.connect()

    def connect(self):

        d  = m.Message(m.TO_SERVER, m.ADD_ME, info={"name": self.name, "suspect": guiToServ[self.name]})

        self.connection.sendLine(pickle.dumps(d))

        if self.startGame:
            d = m.Message(m.TO_SERVER, m.START_GAME)
            self.connection.sendLine(pickle.dumps(d))

    def handle_action(self, line):
        mes = pickle.loads(line)
        if mes.direction == m.FROM_SERVER:
            if mes.typ == m.START:
                self.startReceived(mes)
            elif mes.typ == m.MADE_MOVE:
                self.madeMoveReceived(mes)
            else:
                print "this message is not handled"

    def startReceived(self, mes):
        cards = mes.info[guiToServ[self.name]]
        newCards = []
        for card in cards:
            newCards.append(servToGui[card])
        self.char.setCards(newCards)

        # keep track of opponents
        players = mes.info['players']
        self.allPlayers = [servToGui[x] for x in players]
        self.opps = filter(lambda x: x != self.name, self.allPlayers)
        self.char.setOpponents(self.opps)

    def madeMoveReceived(self, mes):
        newBoard = pickle.loads(mes.info['board'])
        for p in self.opps:
            newX, newY = newBoard.find_player(guiToServ[p])
            self.char.opponents[p].updateLocation(newX, newY)
