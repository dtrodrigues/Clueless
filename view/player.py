import pygame, sys
from pygame.locals import *
import pickle

from pgu import gui

import board, notebook, player_selection, suggestion, accusation, card
from sector import Sector
import logic.message as m
import view.client

ROOMWIDTH = 128
ROOMHEIGHT = 128
HALLWIDTH = 88
HALLHEIGHT = 88

ROOMOFFSET_X = 80
ROOMOFFSET_Y = 60
HALLOFFSET_X = 100
HALLOFFSET_Y = 80

XMAX = 4
YMAX = 4

class Suspect(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        if name == "green":
            self.xOffset = 10
            self.yOffset = 20
        elif name == 'mustard':
            self.xOffset = 20
            self.yOffset = 50
        elif name == 'peacock':
            self.xOffset = 30
            self.yOffset = 20
        elif name == 'plum':
            self.xOffset = 40
            self.yOffset = 50
        elif name == 'scarlet':
            self.xOffset = 50
            self.yOffset = 20
        else: # name == 'white'
            self.xOffset = 60
            self.yOffset = 50
        self.location = self.getStartingLocation()
        self.image = pygame.image.load("view/images/"+name+".png")
        self.rect = self.image.get_rect()

    def getStartingLocation(self):
        if self.name == "scarlet":
            location = Sector(3,0,'')
        elif self.name == 'green':
            location = Sector(1,4,'')
        elif self.name == 'mustard':
            location = Sector(4,1,'')
        elif self.name == 'peacock':
            location = Sector(0,3,'')
        elif self.name == 'plum':
            location = Sector(0,1,'')
        else: # White
            location = Sector(3,4,'')
        return location

    def updateLocation(self, x, y):
        self.location = Sector(x, y, '')

class Character(Suspect):
    def __init__(self, name): #, screen):
        Suspect.__init__(self, name)

        self.name = name
        
        self.board = board.Board()
        #self.board.ShowSplash()
        self.screen = self.board.screen
        self.getStartingLocation()
        
        self.image = pygame.image.load("view/images/"+name+".png")
        self.rect = self.image.get_rect()
        
        self.cards = []
        self.opponents = {}

        self.notebook = notebook.Notebook() #self.nb_surface)

        self.suggestion = suggestion.Suggestion()
        self.accusation = accusation.Accusation()
        self.viewCards = card.ViewCard(self.cards)
        
        
    def setCards(self, cardList):

        self.cards = [card.Card(crd) for crd in cardList]
        self.viewCards = card.ViewCard(self.cards)
        
    def setOpponents(self, opps):
        for opp in opps:
            self.opponents[opp] = Suspect(opp)
    
    def move(self, requested_location):
        #if requested_location in self.board.valid_locations:
        if requested_location in self.location.neighbors:
            self.location.update(requested_location[0], requested_location[1])
            return True
        return False

    def make_suggestion(self):
        if self.location.pos in self.board.rooms.keys():
            room = self.board.rooms[self.location.pos]
            self.suggestion.create(room)
            suspect = self.suggestion.suspect.value
            weapon = self.suggestion.weapon.value
            if suspect in self.opponents.keys():
                self.opponents[suspect].location.update(self.location.x, self.location.y)
            self.update()
            
    def make_accusation(self):
        if self.location.pos in self.board.rooms.keys():
            self.accusation.create()
            suspect = self.accusation.suspect.value
            weapon = self.accusation.weapon.value
            room = self.accusation.room.value

    def view_cards(self):
        self.viewCards.create()

    def update(self):
        # Update the display with the locations of all player tokens
        for opponent in self.opponents.values():
            self.screen.blit(opponent.image, (opponent.xOffset + opponent.location.x * ROOMWIDTH + ROOMOFFSET_X, \
                                              opponent.yOffset + opponent.location.y * ROOMHEIGHT + ROOMOFFSET_Y))
        self.screen.blit(self.image, (self.xOffset + self.location.x * ROOMWIDTH + ROOMOFFSET_X,\
                                      self.yOffset + self.location.y * ROOMHEIGHT + ROOMOFFSET_Y))
        pygame.display.flip()
        
class ClueGUI:

    def __init__(self):
        pass

    def initiate_game(self):

        valid_players = ['green', 'mustard', 'peacock', 'plum', 'scarlet', 'white']
        player_name = ''
        
        while player_name not in valid_players:
        
            p = player_selection.PlayerSelection(valid_players)
            p.start()
            player_name = p.p.value
            # Update valid_players with info from server
            
        player = Character(str(player_name)) #, myBoard.screen)
        self.char = player
        return player_name, self.char
        #start_playing(player)

    def start_playing(self):
        
        clock = pygame.time.Clock()

        while True:
            one_lap()
            clock.tick(120)
            
        sys.exit()

    def make_move(self, newx, newy):
        if self.char.move((newx, newy)):
            d = m.Message(m.TO_SERVER, m.MAKE_MOVE,info={'suspect': view.client.guiToServ[self.char.name], 'coord': (newx,newy)},comment="test")
            self.client.connection.sendLine(pickle.dumps(d))
            
    def one_lap(self):        
            
        GAMEOVER = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAMEOVER = True
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                newx, newy = self.char.location.x+1, self.char.location.y
                self.make_move(newx, newy)
            elif event.type == KEYDOWN and event.key == K_LEFT:
                newx, newy = self.char.location.x-1, self.char.location.y
                self.make_move(newx, newy)
            elif event.type == KEYDOWN and event.key == K_UP:
                newx, newy = self.char.location.x, self.char.location.y-1
                self.make_move(newx, newy)
            elif event.type == KEYDOWN and event.key == K_DOWN:
                newx, newy = self.char.location.x, self.char.location.y+1
                self.make_move(newx, newy)
            elif event.type == KEYDOWN and event.key == K_q:
                GAMEOVER = True
            elif event.type == KEYDOWN and event.key == K_p:
                if self.char.location.x == 0 and self.char.location.y == 0:
                    self.make_move(XMAX, YMAX)
                elif self.char.location.x == 0 and self.char.location.y == YMAX:
                    self.make_move(XMAX, 0)
                elif self.char.location.x == XMAX and self.char.location.y == 0:
                    self.make_move(0, YMAX)
                elif self.char.location.x == XMAX and self.char.location.y == YMAX:
                    self.make_move(0, 0)
            elif event.type == MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if self.char.board.btn_exit.pressed(mouse):        # Exit game
                    GAMEOVER = True
                if self.char.board.btn_notebook.pressed(mouse): # View Notebook
                    self.char.notebook.start()
                if self.char.board.btn_suggest.pressed(mouse): # Make a Suggestion
                    self.char.make_suggestion()
                if self.char.board.btn_accuse.pressed(mouse): # Make an Accusation
                    self.char.make_accusation()
                if self.char.board.btn_cards.pressed(mouse):
                    self.char.view_cards()
                for cell in self.char.board.cells:
                    if cell.clicked(mouse):
                        self.make_move(cell.x, cell.y)

        self.char.screen.blit( self.char.board.background, (0,0) )
        self.char.update()
        pygame.display.flip()
        if GAMEOVER:
            from twisted.internet import reactor
            reactor.callFromThread(reactor.stop)


if __name__ == '__main__':
    print "don't run as main. use ./run-client"
