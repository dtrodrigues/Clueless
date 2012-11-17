#!/usr/bin/env python

import pygame, sys
from pgu import gui

class Suggestion():
    def __init__(self, screen = None):

        self.screen = screen
        self.WIDTH = 400
        self.HEIGHT = 400

    def create(self, room):
        
        self.app = gui.Desktop()
        self.container = gui.Container(width=400, height=400)
        
        self.app.connect(gui.QUIT, self.app.quit, None)
        
        self.suspect = gui.Select(value = 'green')
        self.suspect.add("Mr. Green", 'green')
        self.suspect.add("Colonel Mustard", 'mustard')
        self.suspect.add("Mrs. Peacock", 'peacock')
        self.suspect.add("Professor Plum", 'plum')
        self.suspect.add("Miss Scarlet", 'scarlet')
        self.suspect.add("Mrs. White", 'white')
        
        self.container.add(self.suspect, 25,250)
        
        self.room = gui.Select(value = room)
        self.room.add(room, room)
        
        self.container.add(self.room, 300, 250)
        
        self.weapon = gui.Select(value = 'candlestick')
        self.weapon.add("Candlestick", 'candlestick')
        self.weapon.add("Knife", 'knife')
        self.weapon.add("Lead Pipe", 'lead_pipe')
        self.weapon.add("Revolver", 'revolver')
        self.weapon.add("Rope", 'rope')
        self.weapon.add("Wrench", 'wrench')
        
        self.container.add(self.weapon, 675, 250)
        
        self.suggest_btn = gui.Button("Make Suggestion")
        self.suggest_btn.connect(gui.CLICK, self.app.quit, None) 
        
        self.container.add(self.suggest_btn, 370,300)

        self.start()

    def start(self):
        self.app.run(self.container)
        
