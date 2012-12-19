#!/usr/bin/env python

import pygame

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

ROOMOFFSET_X = 10
ROOMOFFSET_Y = 10
HALLOFFSET_X = 30
HALLOFFSET_Y = 30


class Sector():
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.neighbors = []
        self.update(x,y)
        self.name = name
        self.font = pygame.font.Font(None, 20)
        self.text = self.font.render(self.name, True, (255,255,255))
        
    def update(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.neighbors = []
        self.addNeighbors()
        
    def addNeighbors(self):
        if self.pos == (0, 0):
            self.neighbors.append((4,4))
            self.neighbors.append((1,0))
            self.neighbors.append((0,1))
        if self.x == 0:                
            if self.y == 1:
                self.neighbors.append((0,0))
                self.neighbors.append((0,2))
            elif self.y == 2:
                self.neighbors.append((0,1))
                self.neighbors.append((0,3))
                self.neighbors.append((1,2))
            elif self.y == 3:
                self.neighbors.append((0,2))
                self.neighbors.append((0,4))
            else: # self.y == 4
                self.neighbors.append((4,0))
                self.neighbors.append((0,3))
                self.neighbors.append((1,4))
        if (self.x == 1) or (self.x == 3):
            self.neighbors.append((self.x-1, self.y))
            self.neighbors.append((self.x+1, self.y))
        elif self.x == 2:
            if self.y == 0:
                self.neighbors.append((1,0))
                self.neighbors.append((2,1))
                self.neighbors.append((3,0))
            elif self.y == 1 or self.y == 3:
                self.neighbors.append((self.x, self.y-1))
                self.neighbors.append((self.x, self.y+1))
            elif self.y == 2:
                self.neighbors.append((1,2))
                self.neighbors.append((2,1))
                self.neighbors.append((3,2))
                self.neighbors.append((2,3))
            else: # self.y == 4
                self.neighbors.append((1,4))
                self.neighbors.append((3,4))
                self.neighbors.append((2,3))
        elif self.x == 4:
            if self.y == 0:
                self.neighbors.append((3,0))
                self.neighbors.append((4,1))
                self.neighbors.append((0,4))
            elif self.y == 1 or self.y == 3:
                self.neighbors.append((4, self.y-1))
                self.neighbors.append((4, self.y+1))
            elif self.y == 2:
                self.neighbors.append((3,2))
                self.neighbors.append((4,1))
                self.neighbors.append((4,3))
            else: #self.y == 4
                self.neighbors.append((0,0))
                self.neighbors.append((3,4))
                self.neighbors.append((4,3))
        
                
        
    def clicked(self, mouse):
        if mouse[0] > self.rectangle.topleft[0]:
            if mouse[1] > self.rectangle.topleft[1]:
                if mouse[0] < self.rectangle.bottomright[0]:
                    if mouse[1] < self.rectangle.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

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
