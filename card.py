import pygame
from pygame.locals import *
from pgu import gui

class Card():
    def __init__(self, name):
        self.name = name
        self.image_name = "images/cards/" + name + "_card.png"
        self.image = pygame.image.load(self.image_name)
        
class ViewCard():
    def __init__(self, cards, screen = None):
        self.cards = cards
        
        self.screen = screen
        self.WIDTH = 400
        self.HEIGHT = 400
        
    def create(self):
        
        self.app = gui.Desktop()
        self.container = gui.Container(width=600, height=600)
        
        self.app.connect(gui.QUIT, self.app.quit, None)
        
        x = 0
        y = 5
        for card in self.cards:            
            self.container.add(gui.Image(card.image_name, align=1), x, y)
            x += 110
            if x > 500:
                x = 0
                y = 200
        
        self.exit_btn = gui.Button("Exit")
        self.exit_btn.connect(gui.CLICK, self.app.quit, None) 
        
        self.container.add(self.exit_btn, 470,500)

        self.start()

    def start(self):
        self.app.run(self.container)



    