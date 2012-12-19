import pickle
import logic.message as m
import card
#from view.player import Character
from player import Character
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
            if mes.typ == m.ADD_PLAYER:
                self.playerAdded(mes)
                #add player behavior goes here
                pass
            elif mes.typ == m.START:
                self.startReceived(mes)
            elif mes.typ == m.MADE_MOVE:
                self.madeMoveReceived(mes)
            elif mes.typ == m.MADE_SUGGESTION:
                self.suggestionReceived(mes)
            elif mes.typ == m.TURN_ENDED:
                self.turnEnded(mes)
            elif mes.typ == m.WAS_DISPROVED:
                self.wasDisproved(mes)
            elif mes.typ == m.WON_GAME:
                self.wonGame(mes)
            elif mes.typ == m.LOST_GAME:
                self.lostGame(mes)
            else:
                print "message direction %d type %d is not handled" % (mes.direction, mes.typ)

    def playerAdded(self,mes):
        newPlayer = mes.info['suspect']
        if servToGui[newPlayer] != self.char.name:
            msg = newPlayer + " has joined the game."
            print msg
            self.char.messages.append(msg)

    def startReceived(self, mes):
        msg = "The game has begun."
        self.char.messages.append(msg)
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
        msg = "current turn: " + servToGui[mes.new_turn]
        self.char.messages.append(msg)

    def madeMoveReceived(self, mes):
        newBoard = pickle.loads(mes.info['board'])
        for p in self.opps:
            newX, newY = newBoard.find_player(guiToServ[p])
            self.char.opponents[p].updateLocation(newX, newY)

    def suggestionReceived(self, mes):
        # update board
        newBoard = pickle.loads(mes.info['board'])
        disprover, cards, whoCantDisprove = mes.info['disprover'], mes.info['cards'], mes.info['whoCantDisprove']
        cards = map(lambda x: servToGui[x], cards)
        suggester = mes.info['suspect']
        
        for p in self.char.allPlayers:
            newX, newY = newBoard.find_player(guiToServ[p])
            self.char.allPlayers[p].updateLocation(newX, newY)

        # print messages for players who cannot disprove
        

        if disprover:
            for plyr in whoCantDisprove:
                msg = "%s cannot disprove the suggestion of %s" % (plyr, suggester)
                self.char.messages.append(msg)

            msg = disprover + " can disprove the suggestion; waiting for them to disprove"
            self.char.messages.append(msg)
            if servToGui[disprover] == self.char.name:
                msg = "please select a card to disprove the suggestion with from %s" % str(cards)
                self.char.messages.append(msg)
                self.char.disprove.create(map(card.Card, cards))
                cardShown = self.char.disprove.choice_value.name
                msg = "you have shown " + cardShown + " to " + suggester
                self.char.messages.append(msg)
                d = m.Message(m.TO_SERVER, m.DISPROVE, info={'showTo': suggester, 'card': cardShown, 'shower': self.char.name})
                self.connection.sendLine(pickle.dumps(d))





        # else somebody can disprove
        # if you made the suggestion: print out the players who cant disprove and say "waiting for x to disprove"
        # if you 

        # if you made the suggestion and nobody can disprove it, print out all players
        # and say its the next persons turn

        # if somebo

        # nobody can disprove
        else:
            msg = "who cant disprove: " + str(whoCantDisprove)
            self.char.messages.append(msg)
            for plyr in whoCantDisprove:
                msg = "%s cannot disprove the suggestion of %s" % (plyr, suggester)
                self.char.messages.append(msg)
            # its your suggestion
            if servToGui[suggester] == self.char.name:
                msg = "nobody can disprove your suggestion. make an accusation or end your turn."
                self.char.messages.append(msg)

            # its somebody else's suggestion
            else:
                msg = "nobody can disprove the suggestion of " + suggester
                self.char.messages.append(msg)


        # if nobody can disprove
        #   if you made suggestion: print out all players and inform you that your suggestion went unproven
        #       prompt you to make an accusation or end turn
        #   if somebody else made suggestion: print out all other players

    def wasDisproved(self, mes):
        nextp = servToGui[mes.new_turn]
        showTo = mes.info['showTo']
        shower = mes.info['shower']
        card = mes.info['card']
        
        # you are being shown the card
        if servToGui[showTo] == self.char.name:
            msg = shower + " has shown you the " + card + " card"
            self.char.messages.append(msg)
            msg = "your turn is now over"
            self.char.messages.append(msg)

        # you are showing the card
        elif shower == self.char.name:
            pass

        # you are neither the shower or the showee
        else:
            msg = shower + " has shown a card to " + showTo
            self.char.messages.append(msg)

        if nextp == self.char.name:
            msg = "it is now your turn"
            self.char.messages.append(msg)
        else:
            msg = "it is now the turn of " + nextp
            self.char.messages.append(msg)

        


    def turnEnded(self, mes):        
        nextP = servToGui[mes.new_turn]
        if nextP == self.char.name:
            msg = "it's your turn"
            self.char.messages.append(msg)
            # check if there are valid moves
            msg = "make a move"
            self.char.messages.append(msg)
        else:
            msg = "it's %s's turn" % mes.new_turn
            self.char.messages.append(msg)


    def wonGame(self, mes):
        accusation = mes.info['accusation']
        suspect = mes.info['suspect']
        msg = suspect + " has made the accusation of " + str(accusation)
        self.char.messages.append(msg)

        #update board
        newBoard = pickle.loads(mes.info['board'])
        for p in self.char.allPlayers:
            newX, newY = newBoard.find_player(guiToServ[p])
            self.char.allPlayers[p].updateLocation(newX, newY)

        msg = "checking accusation"
        self.char.messages.append(msg)
        if servToGui[suspect] == self.char.name:
            msg = "Congratulations. You have won the game"
            self.char.messages.append(msg)
        else:
            msg = suspect + " has won the game!"
            self.char.messages.append(msg)
        msg = "The game is over"
        self.char.messages.append(msg)

    def lostGame(self, mes):
        accusation = mes.info['accusation']
        suspect = mes.info['suspect']
        msg = suspect + " has made the accusation of " + str(accusation)
        self.char.messages.append(msg)
        msg = "checking accusation"
        self.char.messages.append(msg)
        if servToGui[suspect] == self.char.name:
            msg = "Your accusation is incorrect. You have lost the game."
            self.char.messages.append(msg)
        else:
            msg = suspect + " has made an incorrect accusation. They have lost the game."
            self.char.messages.append(msg)

        #update board
        newBoard = pickle.loads(mes.info['board'])
        for p in self.char.allPlayers:
            newX, newY = newBoard.find_player(guiToServ[p])
            self.char.allPlayers[p].updateLocation(newX, newY)

        self.turnEnded(mes)


