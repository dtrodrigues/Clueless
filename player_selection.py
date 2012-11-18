#!/usr/bin/env python

import pygame, sys
from pgu import gui

class PlayerSelection():
    def __init__(self, valid_players, screen = None):

        self.screen = screen
        #self.WIDTH = 400
        #self.HEIGHT = 400

        self.app = gui.Desktop()
        self.container = gui.Container(width=1000, height=750)
        
        self.app.connect(gui.QUIT, self.app.quit, None)
        
        self.msg = gui.Label('Please select a player')
        self.container.add(self.msg, 450, 150)
        
        self.p = gui.Select(value = 'green')
        if 'green' in valid_players:
            self.p.add("Mr. Green", 'green')
        if 'mustard' in valid_players:
            self.p.add("Colonel Mustard", 'mustard')
        if 'peacock' in valid_players:
            self.p.add("Mrs. Peacock", 'peacock')
        if 'plum' in valid_players:
            self.p.add("Professor Plum", 'plum')
        if 'scarlet' in valid_players:
            self.p.add("Miss Scarlet", 'scarlet')
        if 'white' in valid_players:
            self.p.add("Mrs. White", 'white')
        
        self.container.add(self.p, 450,250)
        
        self.join_btn = gui.Button("Join Game")
        self.join_btn.connect(gui.CLICK, self.app.quit, None) 

        self.container.add(self.join_btn, 470,500)


    def start(self):
        self.app.run(self.container)
        
