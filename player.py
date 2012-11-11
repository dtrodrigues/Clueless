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
        green = Opponent('green')
        mustard = Opponent('mustard')
        plum = Opponent('plum')
        peacock = Opponent('peacock')
        scarlet = Opponent('scarlet')
        white = Opponent('white')
        if self.name != 'mustard':
            self.opponents.append(mustard)
        if self.name != 'plum':
            self.opponents.append(plum)
        if self.name != 'peacock':
            self.opponents.append(peacock)
        if self.name != 'scarlet':
            self.opponents.append(scarlet)
        if self.name != 'white':
            self.opponents.append(white)
        if self.name != 'green':
            self.opponents.append(green)
        
    def getStartingLocation(self):
        if self.name == "scarlet":
            location = board.Sector(3,0,'')
        elif self.name == 'green':
            location = board.Sector(1,4,'')
        elif self.name == 'mustard':
            location = board.Sector(4,1,'')
        elif self.name == 'peacock':
            location = board.Sector(0,3,'')
        elif self.name == 'plum':
            location = board.Sector(0,1,'')
        else: # White
            location = board.Sector(3,4,'')
        return location
    
    def move(self, requested_location):
        #if requested_location in self.board.valid_locations:
        if requested_location in self.location.neighbors:
            self.location = board.Sector(requested_location[0], requested_location[1], '')

    def update(self):
        # Update the display with the locations of all player tokens
        for opponent in self.opponents:
            self.screen.blit(opponent.image, (opponent.xOffset + opponent.location.x * ROOMWIDTH + ROOMOFFSET_X, \
                                              opponent.yOffset + opponent.location.y * ROOMHEIGHT + ROOMOFFSET_Y))
        self.screen.blit(self.image, (self.xOffset + self.location.x * ROOMWIDTH + ROOMOFFSET_X,\
                                      self.yOffset + self.location.y * ROOMHEIGHT + ROOMOFFSET_Y))
        pygame.display.flip()
        

def main():

    print ("Available players are:")
    print ("Mr. Green (green)")
    print ("Colonel Mustard (mustard)")
    print ("Mrs. Peacock (peacock)")
    print ("Professor Plum (plum)")
    print ("Miss Scarlet (scarlet)")
    print ("Mrs. White (white)")
    
    player_name = raw_input("Please select a player:  ")
        
    player = Character(str(player_name)) #, myBoard.screen)
    start_playing(player)

def start_playing(player):
    

    GAMEOVER = False

    clock = pygame.time.Clock()

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
                for cell in player.board.cells:
                    if cell.clicked(mouse):
                        player.move((cell.x, cell.y))

        player.screen.blit( player.board.background, (0,0) )
        player.update()
        pygame.display.flip()
    

    sys.exit()

if __name__ == '__main__':
    main()