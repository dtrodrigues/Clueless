import pygame, sys
from pygame.locals import *

from pgu import gui

import board, notebook

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

clock = pygame.time.Clock()

class Opponent(pygame.sprite.Sprite):
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
            location = board.Sector(3,0,"")
        elif self.name == 'green':
            location = board.Sector(1,4,'')
        elif self.name == 'mustard':
            location = board.Sector(4,1,'')
        elif self.name == 'peacock':
            location = board.Sector(0,3,'')
        elif self.name == 'plum':
            location = board.Sector(0,1,'')
        else: # White
            location = board.Sector(3,4,"")
        return location


class Character(pygame.sprite.Sprite):
    def __init__(self, name): #, screen):
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
        
        self.board = board.Board()
        self.board.ShowSplash()
        self.screen = self.board.screen
        self.location = self.getStartingLocation()
        
        self.image = pygame.image.load("images/"+name+".png")
        self.rect = self.image.get_rect()

        self.opponents = []
        self.getOpponents()

#        self.nb_surface = pygame.Surface((400,640))
        self.notebook = notebook.Notebook() #self.nb_surface)
#        self.screen.blit(self.nb_surface,(100,100))
#        pygame.display.flip()
        
    def getOpponents(self):
        self.opponents.append(Opponent('mustard'))
        self.opponents.append(Opponent('plum'))
        self.opponents.append(Opponent('peacock'))
        self.opponents.append(Opponent('scarlet'))
        self.opponents.append(Opponent('white'))

    def getStartingLocation(self):
        if self.name == "scarlet":
            location = board.Sector(3,0,"")
        elif self.name == 'green':
            location = board.Sector(1,4,'')
        elif self.name == 'mustard':
            location = board.Sector(4,1,'')
        elif self.name == 'peacock':
            location = board.Sector(0,3,'')
        elif self.name == 'plum':
            location = board.Sector(0,1,'')
        else: # White
            location = board.Sector(3,4,"")
        return location
    
    def move(self, requested_location):
        if requested_location in self.board.valid_locations:
            self.location.x = requested_location[0]
            self.location.y = requested_location[1]

    def update(self):
        # Update the display with the locations of all player tokens
        for opponent in self.opponents:
            opponent.location.x = 2
            opponent.location.y = 2
            self.screen.blit(opponent.image, (opponent.xOffset + opponent.location.x * ROOMWIDTH + ROOMOFFSET_X, \
                                              opponent.yOffset + opponent.location.y * ROOMHEIGHT + ROOMOFFSET_Y))
        self.screen.blit(self.image, (self.xOffset + self.location.x * ROOMWIDTH + ROOMOFFSET_X,\
                                      self.yOffset + self.location.y * ROOMHEIGHT + ROOMOFFSET_Y))
        pygame.display.flip()
        
#myBoard = board.Board()
#myBoard.ShowSplash()

player = Character("green") #, myBoard.screen)

GAMEOVER = False

while not GAMEOVER:
    
    clock.tick(120)
    
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
            #if myBoard.btn_exit.pressed(mouse):	#Exit the game
            if player.board.btn_exit.pressed(mouse):
                GAMEOVER = True
            elif player.board.btn_notebook.pressed(mouse): # View Notebook
                player.notebook.start()
    player.screen.blit( player.board.background, (0,0) )
    player.update()
    pygame.display.flip()
    

sys.exit()
