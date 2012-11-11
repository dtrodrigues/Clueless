import pygame, sys
from pgu import gui
from pygame.locals import *
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

class Character(pygame.sprite.Sprite):
    def __init__(self, name, screen):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.xOffset = 50
        self.yOffset = 50
        self.screen = screen
        self.location = self.getStartingLocation()
        self.color = self.getColor()
        
        self.image = pygame.image.load("images/"+name+".png")
        #self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.nb_surface = pygame.Surface((400,640))
        self.notebook = notebook.Notebook(self.nb_surface)
        self.screen.blit(self.nb_surface,(100,100))
        pygame.display.flip()
        
    def getStartingLocation(self):
        if self.name == "scarlet":
            location = board.Sector(3,0,"")
        else:
            location = board.Sector(4,4,"")
        return location
    
    def getColor(self):
        if self.name == "scarlet":
            color = (255,0,0)
        else:
            color = (0,255,0)
        return color
        
    def update(self):
        self.screen.blit(self.image, (self.xOffset + self.location.x * ROOMWIDTH + ROOMOFFSET_X,\
                                      self.yOffset + self.location.y * ROOMHEIGHT + ROOMOFFSET_Y))
        pygame.display.flip()
        
myBoard = board.Board()
myBoard.ShowSplash()

player = Character("scarlet", myBoard.screen)

GAMEOVER = False
moved = False
while not GAMEOVER:
    
    clock.tick(120)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMEOVER = True
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if player.location.x < XMAX and player.location.y % 2 == 0:
                player.location.x += 1
                moved = True
        elif event.type == KEYDOWN and event.key == K_LEFT:
            if player.location.x > 0 and player.location.y % 2 == 0:
                player.location.x -= 1
                moved = True
        elif event.type == KEYDOWN and event.key == K_UP:
            if player.location.y > 0 and player.location.x % 2 == 0:
                player.location.y -= 1
        elif event.type == KEYUP and event.key == K_DOWN:
            if player.location.y < YMAX and player.location.x % 2 == 0:
                player.location.y += 1
        elif event.type == KEYDOWN and event.key == K_p:
            if player.location.x == 0 and player.location.y == 0:
                player.location.x = XMAX
                player.location.y = YMAX
            elif player.location.x == 0 and player.location.y == YMAX:
                player.location.x = XMAX
                player.location.y = 0
            elif player.location.x == XMAX and player.location.y == 0:
                player.location.x = 0
                player.location.y = YMAX
            elif player.location.x == XMAX and player.location.y == YMAX:
                player.location.x = 0
                player.location.y = 0
        elif event.type == MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if myBoard.btn_exit.pressed(mouse):	#Exit the game
                GAMEOVER = True
            elif myBoard.btn_notebook.pressed(mouse): # View Notebook
                player.notebook.start()
    player.screen.blit( myBoard.background, (0,0) )
    player.update()
    pygame.display.flip()
    

sys.exit()
