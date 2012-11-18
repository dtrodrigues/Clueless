import pygame
from pygame.locals import *

class Card():
    def __init__(self, name):
        self.name = name
        self.image = pygame.image.load("images/cards"+name+"_card.png")