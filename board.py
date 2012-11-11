#!/usr/local/bin/python2.7

import pygame
from pgu import gui

import time
from pygame.locals import *

import button

# Some constants

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
PASSAGE = 4

ROOM = 0
HHALL = 1
VHALL = 2

ROOMWIDTH = 128
ROOMHEIGHT = 128
HALLWIDTH = 88
HALLHEIGHT = 88

ROOMOFFSET_X = 80
ROOMOFFSET_Y = 60
HALLOFFSET_X = 100
HALLOFFSET_Y = 80


class Board:
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption('Clued-In')
        self.screen = pygame.display.set_mode((1000,750), pygame.DOUBLEBUF)
        GAMEOVER = False
        
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((184, 138, 65))
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        
        self.btn_notebook = button.Button('button_notebook')
        self.btn_suggest = button.Button('button_suggest')
        self.btn_accuse = button.Button('button_accuse')
        self.btn_exit = button.Button('button_close')
               

        self.cells = []
        self.valid_locations = []
        
        self.ShowMap()
            
           
#        while not GAMEOVER:
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    GAMEOVER = True
    
    def ShowSplash(self):
        splashImg = pygame.image.load('images/splash_screen.png')
        
        self.screen.blit(splashImg, (50,50))
        pygame.display.flip()
        time.sleep(2)
        
            
    def ShowMap(self):
        for x in range(0,5):
            for y in range(0,5):
                passage = False
                if x % 2 == 0 and (y % 2 == 0):       # This is a Room
                    pos = (x,y)
                    if pos == (0, 0):
                        name = "Study"
                        passage = True
                    elif pos == (2, 0):
                        name = "Hall"
                    elif pos == (4, 0):
                        name = "Lounge"
                        passage = True
                    elif pos == (0, 2):
                        name = "Library"
                    elif pos == (2, 2):
                        name = "Billiard Room"
                    elif pos == (4, 2):
                        name = "Dining Room"
                    elif pos == (0, 4):
                        name = "Conservatory"
                        passage = True
                    elif pos == (2, 4):
                        name = "Dining Room"
                    elif pos == (4, 4):
                        name = "Kitchen"
                        passage = True
                    else:
                        name = "Default"
                    self.cells.append(Room(x, y, name, passage))
                    self.valid_locations.append(pos)
                elif x % 2 == 0 or (y % 2 == 0):
                    self.cells.append(Hallway(x,y, "Hallway"))
                    self.valid_locations.append((x,y))
                else:
                    name = ''

        # clear the screen first
                
        for cell in self.cells:
            
            pygame.draw.rect(self.background, cell.color, cell.rectangle, 0)
            self.background.blit(cell.text, cell.rectangle)
            if cell.hasPassage:
                pygame.draw.rect(self.background, (0,0,0), cell.pRectangle, 0)
                self.background.blit(cell.pText, cell.pRectangle)
        
        
        # Add event buttons button
        self.btn_notebook.setCords(ROOMWIDTH * 6.5, ROOMHEIGHT * 3)
        self.btn_suggest.setCords(ROOMWIDTH * 6.5, ROOMHEIGHT * 3.5)
        self.btn_accuse.setCords(ROOMWIDTH * 6.5, ROOMHEIGHT * 4)
        self.btn_exit.setCords(ROOMWIDTH * 6.5, ROOMHEIGHT * 5)
        
        self.background.blit(self.btn_notebook.image, self.btn_notebook.rect.topleft)
        self.background.blit(self.btn_suggest.image, self.btn_suggest.rect.topleft)
        self.background.blit(self.btn_accuse.image, self.btn_accuse.rect.topleft)
        self.background.blit(self.btn_exit.image, self.btn_exit.rect.topleft)
        pygame.display.flip()
        
        self.screen.blit( self.background, (0,0) )
        pygame.display.flip()
        
        
class Quit(gui.Button):
    def __init__(self, **params):
        params['value'] = 'Quit'
        gui.Button.__init__(self,**params)
        self.connect(gui.CLICK, app.quit, None)



class Sector():
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.font = pygame.font.Font(None, 20)
        self.text = self.font.render(self.name, True, (255,255,255))
        
class Room(Sector):
    def __init__(self, x, y, name, passage):
        Sector.__init__(self, x, y, name)
        self.xPos = ROOMOFFSET_X + self.x*ROOMWIDTH
        self.yPos = ROOMOFFSET_Y + self.y*ROOMHEIGHT
        self.rectangle = pygame.Rect( (self.xPos, self.yPos, ROOMWIDTH, \
                                       ROOMHEIGHT) )
        self.color = (150, 150, 200)
        self.hasPassage = passage
        if self.hasPassage:
            self.pRectangle = pygame.Rect( (self.xPos + ROOMWIDTH - 30, \
                                            self.yPos + ROOMHEIGHT - 30, \
                                            30, 30) )
            self.pText = self.font.render("P", True, (255,255,255))
        
        
        

class Hallway(Sector):
    def __init__(self, x, y, name=""):
        Sector.__init__(self, x, y, name)
        if x % 2 == 1:
            # Vertical Hallway
            self.rectangle = pygame.Rect( (ROOMOFFSET_X + x*128, HALLOFFSET_Y + y*128, ROOMWIDTH, HALLHEIGHT) ) 
        else:
            # Horizontal Hallway
            self.rectangle = pygame.Rect( (HALLOFFSET_X + x*128, ROOMOFFSET_Y + y*128, HALLWIDTH, ROOMHEIGHT) )
        self.color = (50, 50, 50)
        self.hasPassage = False


                
mygui = Board()
