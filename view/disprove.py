import pygame
from pygame.locals import *
from pgu import gui


class Disprove():
    def __init__(self, screen = None):
        
        self.screen = screen
        self.WIDTH = 400
        self.HEIGHT = 400

        
    def create(self, cards):
        self.cards = cards

        self.choice_value = self.cards[0]
        
        self.app = gui.Desktop()
        self.container = gui.Container(width=600, height=600)
        
        self.app.connect(gui.QUIT, self.app.quit, None)
        
        self.msg = gui.Label("Choose a card to disprove the suggestion.")
        
        self.container.add(self.msg, 10,0)
        
        self.choice = gui.Group(name="Card", value = self.choice_value)
        
        x = 0
        y = 25
        for card in self.cards:            
            self.container.add(gui.Image(card.image_name, align=1), x, y)
            self.container.add(gui.Radio(self.choice, value=card), x+50, y+150)
            x += 110
            if x > 500:
                x = 0
                y += 200
        
        self.show_btn = gui.Button("Show Card")
        self.show_btn.connect(gui.CLICK, self.app.quit, None) 
        
        self.container.add(self.show_btn, 470,500)

        self.start()

    def start(self):
        self.app.run(self.container)

