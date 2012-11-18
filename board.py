#!/usr/local/bin/python2.7

import pygame
from pgu import gui

import time
from pygame.locals import *

import button
from sector import *

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
        self.btn_cards = button.Button('button_cards')
        self.btn_exit = button.Button('button_close')
               

        self.cells = []
        
        self.rooms = {(0,0):"Study",
                      (0,2):"Libary",
                      (0,4):"Conservatory",
                      (2,0):"Hall",
                      (2,2):"Billiard Room",
                      (2,4):"Ballroom",
                      (4,0):"Lounge",
                      (4,2):"Dining Room",
                      (4,4):"Kitchen"
                     }
        
        self.ShowMap()
        
               
    def ShowSplash(self):
        splashImg = pygame.image.load('images/splash_screen.png')
        
        self.screen.blit(splashImg, (50,50))
        pygame.display.flip()
        time.sleep(2)
        
            
    def ShowMap(self):
        for x in range(0,5):
            for y in range(0,5):
                passage = False
#                if x % 2 == 0 and (y % 2 == 0):       # This is a Room
                if (x,y) in self.rooms.keys():         # This is a room
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
                elif x % 2 == 0 or (y % 2 == 0):
                    self.cells.append(Hallway(x,y, "Hallway"))
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
        self.btn_cards.setCords(ROOMWIDTH * 6.5, ROOMHEIGHT * 4.5)
        self.btn_exit.setCords(ROOMWIDTH * 6.5, ROOMHEIGHT * 5)
        
        self.background.blit(self.btn_notebook.image, self.btn_notebook.rect.topleft)
        self.background.blit(self.btn_suggest.image, self.btn_suggest.rect.topleft)
        self.background.blit(self.btn_accuse.image, self.btn_accuse.rect.topleft)
        self.background.blit(self.btn_cards.image, self.btn_cards.rect.topleft)
        self.background.blit(self.btn_exit.image, self.btn_exit.rect.topleft)
        pygame.display.flip()
        
        self.screen.blit( self.background, (0,0) )
        pygame.display.flip()
        
        
class Quit(gui.Button):
    def __init__(self, **params):
        params['value'] = 'Quit'
        gui.Button.__init__(self,**params)
        self.connect(gui.CLICK, app.quit, None)





def main():                
    mygui = Board()
    
if __name__ == '__main__':
    main()
