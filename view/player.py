import pygame, sys
from pygame.locals import *
import pickle

from pgu import gui

import board, notebook, player_selection, suggestion, accusation, card, disprove
from sector import Sector

import view.client

ROOMWIDTH = 128
ROOMHEIGHT = 128
HALLWIDTH = 88
HALLHEIGHT = 88

ROOMOFFSET_X = 10
ROOMOFFSET_Y = 10
HALLOFFSET_X = 30
HALLOFFSET_Y = 30

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
        self.fancy_name = self.getFancyName()
        self.color = self.getColor()

    def getFancyName(self):
        if self.name == 'green':
            fancy_name = 'Mr. Green'
        elif self.name == 'mustard':
            fancy_name = 'Colonel Mustard'
        elif self.name == 'peacock':
            fancy_name = 'Mrs. Peacock'
        elif self.name == 'plum':
            fancy_name = 'Professor Plum'
        elif self.name == 'scarlet':
            fancy_name = 'Miss Scarlet'
        else: # self.name == 'white'
            fancy_name = 'Mrs. White'
        return fancy_name
    
    def getColor(self):
        if self.name == 'mustard':
            color = [255,255,0]
        elif self.name == 'green':
            color = [0,255,0]
        elif self.name == 'peacock':
            color = [0,0,255]
        elif self.name == 'plum':
            color = [100,0,255]
        elif self.name == 'scarlet':
            color = [255,0,0]
        else: # self.name == 'white'
            color = [255,255,255]
        return color


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
    def __init__(self, name, screen):
        Suspect.__init__(self, name)

        self.name = name
        
        self.board = board.Board(screen)
        #self.board.ShowSplash()
        #self.screen = self.board.screen

        self.screen = screen
        self.getStartingLocation()
        
        self.image = pygame.image.load("view/images/"+name+".png")
        self.rect = self.image.get_rect()
        
        self.cards = []
        self.opponents = {}
        self.allPlayers = self.opponents.copy()
        self.allPlayers[self.name] = self

        self.messages = []

        self.notebook = notebook.Notebook() #self.nb_surface)

        self.suggestion = suggestion.Suggestion()
        self.accusation = accusation.Accusation()
        self.viewCards = card.ViewCard(self.cards)

        self.disprove = disprove.Disprove()

        self.displayNames()

    def displayNames(self):
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(self.fancy_name, True, self.color)
        x = 1
        self.text_rect = pygame.Rect(ROOMWIDTH*6, ROOMHEIGHT*5, 50, 50)
        self.board.background.blit(self.text, self.text_rect)
            
        for o in self.opponents.values(): # Show player list
            self.text = self.font.render(o.fancy_name, True, o.color)
            self.text_rect = pygame.Rect(ROOMWIDTH*6, ROOMHEIGHT*5+30*x, 50, 50)
            self.board.background.blit(self.text, self.text_rect)
            x += 1
        pygame.display.flip()
        
    def setCards(self, cardList):

        self.cards = [card.Card(crd) for crd in cardList]
        self.viewCards = card.ViewCard(self.cards)
        
    def setOpponents(self, opps):
        for opp in opps:
            self.opponents[opp] = Suspect(opp)
        self.displayNames()
    
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
            return True, view.client.servToGui[room], suspect, weapon
        else:
            print "you must be in a room to make a suggestion"
            return False, None, None, None



    def make_accusation(self):
        self.accusation.start()
        suspect = self.accusation.suspect.value
        weapon = self.accusation.weapon.value
        room = self.accusation.room.value
        return suspect, weapon, room

    def view_cards(self):
        self.viewCards.start()

    def update(self):
        # Update the display with the locations of all player tokens
        for opponent in self.opponents.values():
            self.screen.blit(opponent.image, (opponent.xOffset + opponent.location.x * ROOMWIDTH + ROOMOFFSET_X,
                                              opponent.yOffset + opponent.location.y * ROOMHEIGHT + ROOMOFFSET_Y))
        self.screen.blit(self.image, (self.xOffset + self.location.x * ROOMWIDTH + ROOMOFFSET_X,
                                      self.yOffset + self.location.y * ROOMHEIGHT + ROOMOFFSET_Y))
        pygame.display.flip()
        
