import pygame
from pygame.locals import *
from pgu import gui

class Card():
    def __init__(self, name):
        self.name = name
        self.image_name = "view/images/cards/" + name + "_card.png"
        self.image = pygame.image.load(self.image_name)
        
class ViewCard(gui.Dialog):
    def __init__(self, cards):
        self.cards = cards
        
        self.title = gui.Label("Cards")
        self.container = gui.Container(width=600, height=600)
        
        x = 0
        y = 5
        for card in self.cards:            
            self.container.add(gui.Image(card.image_name, align=1), x, y)
            x += 110
            if x > 500:
                x = 0
                y = 200
        
        self.exit_btn = gui.Button("Exit")
        self.exit_btn.connect(gui.CLICK, self.close) 
        
        self.container.add(self.exit_btn, 470,500)


    def start(self):
        gui.Dialog.__init__(self, self.title, self.container)
        self.open()



    
