import pygame, sys
from pygame.locals import *

from pgu import gui

import board, notebook, player_selection, suggestion, accusation, card
from sector import Sector

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
        self.image = pygame.image.load("images/"+name+".png")
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
            location = Sector(3,4,"")
        return location


class Character(Suspect):
    def __init__(self, name): #, screen):
        Suspect.__init__(self, name)
        
        self.board = board.Board()
        #self.board.ShowSplash()
        self.screen = self.board.screen
        self.getStartingLocation()
        
        self.image = pygame.image.load("images/"+name+".png")
        self.rect = self.image.get_rect()
        
        self.cards = self.getCards()

        self.opponents = {}
        self.getOpponents()

        self.notebook = notebook.Notebook() #self.nb_surface)

        self.suggestion = suggestion.Suggestion()
        self.accusation = accusation.Accusation()
        self.viewCards = card.ViewCard(self.cards)
        
        
    def getCards(self):
        cards = []
        cards.append(card.Card('green'))
        cards.append(card.Card('rope'))
        cards.append(card.Card('revolver'))
        cards.append(card.Card('wrench'))
        cards.append(card.Card('library'))
        cards.append(card.Card('candlestick'))
        cards.append(card.Card('lead'))
        return cards
        
        
    def getOpponents(self):
        green = Suspect('green')
        mustard = Suspect('mustard')
        plum = Suspect('plum')
        peacock = Suspect('peacock')
        scarlet = Suspect('scarlet')
        white = Suspect('white')
        if self.name != 'mustard':
            self.opponents['mustard'] = (mustard)
        if self.name != 'plum':
            self.opponents['plum'] = (plum)
        if self.name != 'peacock':
            self.opponents['peacock'] = (peacock)
 #       if self.name != 'scarlet':
 #           self.opponents.append(scarlet)
        #if self.name != 'white':
            #self.opponents.append(white)
        #if self.name != 'green':
         #   self.opponents.append(green)
                
    
    def move(self, requested_location):
        #if requested_location in self.board.valid_locations:
        if requested_location in self.location.neighbors:
            self.location.update(requested_location[0], requested_location[1])

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
        

def main():
    
    valid_players = ['green', 'mustard', 'peacock', 'plum', 'scarlet', 'white']
    player_name = ''
    
    while player_name not in valid_players:
    
        p = player_selection.PlayerSelection(valid_players)
        p.start()
        player_name = p.p.value
        
    player = Character(str(player_name)) #, myBoard.screen)
    start_playing(player)

def start_playing(player):
    
    clock = pygame.time.Clock()

    while True:
        one_lap(player)
        clock.tick(120)
        
    sys.exit()

        
def one_lap(player):        
        
    GAMEOVER = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMEOVER = True
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            player.move((player.location.x+1, player.location.y))
        elif event.type == KEYDOWN and event.key == K_LEFT:
            player.move((player.location.x-1, player.location.y))
        elif event.type == KEYDOWN and event.key == K_UP:
            player.move((player.location.x, player.location.y-1))
        elif event.type == KEYUP and event.key == K_DOWN:
            player.move((player.location.x, player.location.y+1))
        elif event.type == KEYDOWN and event.key == K_p:
            if player.location.x == 0 and player.location.y == 0:
                player.move((XMAX, YMAX))
            elif player.location.x == 0 and player.location.y == YMAX:
                player.move((XMAX, 0))
            elif player.location.x == XMAX and player.location.y == 0:
                player.move((0, YMAX))
            elif player.location.x == XMAX and player.location.y == YMAX:
                player.move((0, 0))
        elif event.type == MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if player.board.btn_exit.pressed(mouse):        # Exit game
                GAMEOVER = True
            if player.board.btn_notebook.pressed(mouse): # View Notebook
                player.notebook.start()
            if player.board.btn_suggest.pressed(mouse): # Make a Suggestion
                player.make_suggestion()
            if player.board.btn_accuse.pressed(mouse): # Make an Accusation
                player.make_accusation()
            if player.board.btn_cards.pressed(mouse):
                player.view_cards()
            for cell in player.board.cells:
                if cell.clicked(mouse):
                    player.move((cell.x, cell.y))

    player.screen.blit( player.board.background, (0,0) )
    player.update()
    pygame.display.flip()
    if GAMEOVER:
        sys.exit()


if __name__ == '__main__':
    main()