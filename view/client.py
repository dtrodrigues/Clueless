import pickle
import logic.message as m
import card
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
            print newPlayer + " has joined the game."

    def startReceived(self, mes):
        print "The game has begun."
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
        print "It is now the turn of " + mes.new_turn + "."

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
        

        sug = mes.info['suggestion']
        print "The suggestion is " + str(sug[1]) + " in the " + str(sug[0]) + " with the " + str(sug[2]) + "."

        if disprover:
            for plyr in whoCantDisprove:
                print "%s cannot disprove the suggestion of %s" % (plyr, suggester)

            print disprover + " can disprove the suggestion; waiting for them to disprove."
            if servToGui[disprover] == self.char.name:
                #print "Please select a card to disprove the suggestion with from %s" % str(cards)
                self.char.disprove.create(map(card.Card, cards))
                cardShown = self.char.disprove.choice_value.name
                print "You have shown " + guiToServ[cardShown] + " to " + suggester
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
#            print "who cant disprove: " + str(whoCantDisprove)
            for plyr in whoCantDisprove:
                print "%s cannot disprove the suggestion of %s" % (plyr, suggester)
            # its your suggestion
            if servToGui[suggester] == self.char.name:
                print "Nobody can disprove your suggestion. Make an accusation or end your turn."

            # its somebody else's suggestion
            else:
                print "Nobody can disprove the suggestion of " + suggester


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
            print guiToServ[shower] + " has shown you the " + guiToServ[card] + " card"
            print "Your turn is now over."

        # you are showing the card
        elif shower == self.char.name:
            pass

        # you are neither the shower or the showee
        else:
            print guiToServ[shower] + " has shown a card to " + showTo + "."

        if nextp == self.char.name:
            print "It's your turn."
            # check if there are valid moves
            print "Make a move."
        else:
            print "It's now the turn of " + guiToServ[nextp]

        


    def turnEnded(self, mes):        
        nextP = servToGui[mes.new_turn]
        if nextP == self.char.name:
            print "It's your turn."
            # check if there are valid moves
            print "Make a move."
        else:
#            print "It's %s's turn" % mes.new_turn
            print "It's now the turn of " + mes.new_turn + "."


    def wonGame(self, mes):
        accusation = mes.info['accusation']
        suspect = mes.info['suspect']
        print suspect + " has made the accusation of " + str(accusation)

        #update board
        newBoard = pickle.loads(mes.info['board'])
        for p in self.char.allPlayers:
            newX, newY = newBoard.find_player(guiToServ[p])
            self.char.allPlayers[p].updateLocation(newX, newY)

        print "Checking accusation."
        if servToGui[suspect] == self.char.name:
            print "Congratulations! You have won the game!"
        else:
            print suspect + " has won the game!"
        print "The game is over."

    def lostGame(self, mes):
        accusation = mes.info['accusation']
        suspect = mes.info['suspect']
        print suspect + " has made the accusation of " + str(accusation)
        print "Checking accusation"
        if servToGui[suspect] == self.char.name:
            print "Your accusation is incorrect. You have lost the game."
        else:
            print suspect + " has made an incorrect accusation. They have lost the game."

        #update board
        newBoard = pickle.loads(mes.info['board'])
        for p in self.char.allPlayers:
            newX, newY = newBoard.find_player(guiToServ[p])
            self.char.allPlayers[p].updateLocation(newX, newY)

        self.turnEnded(mes)


