#!/usr/bin/env python

import pygame, sys
from pgu import gui

class PlayerSelection():
    def __init__(self, screen = None):

        self.screen = screen
        #self.WIDTH = 400
        #self.HEIGHT = 400

        self.app = gui.Desktop()
        self.container = gui.Container(width=1000, height=750)
        
        self.app.connect(gui.QUIT, self.app.quit, None)
        
        self.p = gui.Select(value = 'green')
        self.p.add("Mr. Green", 'green')
        self.p.add("Colonel Mustard", 'mustard')
        self.p.add("Mrs. Peacock", 'peacock')
        self.p.add("Professor Plum", 'plum')
        self.p.add("Miss Scarlet", 'scarlet')
        self.p.add("Mrs. White", 'white')
        
        self.container.add(self.p, 450,250)
        
        self.join_btn = gui.Button("Join Game")
        self.join_btn.connect(gui.CLICK, self.app.quit, None) 

        self.container.add(self.join_btn, 470,500)


    def start(self):
        self.app.run(self.container)
        
