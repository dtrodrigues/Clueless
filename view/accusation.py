#!/usr/bin/env python

import pygame, sys
from pgu import gui

class Accusation(gui.Dialog):
    def __init__(self):

        self.title = gui.Label("Make Accusation")

        self.container = gui.Container(width=100, height=150)

        self.label = gui.Label("Accuse a suspect, room, and weapon.")
        self.container.add(self.label, 0, 0)
        
        self.suspect = gui.Select(value = 'green')
        self.suspect.add("Mr. Green", 'green')
        self.suspect.add("Colonel Mustard", 'mustard')
        self.suspect.add("Mrs. Peacock", 'peacock')
        self.suspect.add("Professor Plum", 'plum')
        self.suspect.add("Miss Scarlet", 'scarlet')
        self.suspect.add("Mrs. White", 'white')
        
        self.container.add(self.suspect, 0,25)
        
        self.room = gui.Select(value = 'Ballroom')
        self.room.add("Ballroom", 'Ballroom')
        self.room.add("Billiard Room", 'Billiard_room')
        self.room.add("Conservatory", 'Conservatory')
        self.room.add("Dining Room", 'Dining_room')
        self.room.add("Hall", 'Hall')
        self.room.add("Kitchen", 'Kitchen')
        self.room.add("Library", 'Library')
        self.room.add("Lounge", 'Lounge')
        self.room.add("Study", 'Study')
        
        self.container.add(self.room, 0, 50)
        
        self.weapon = gui.Select(value = 'candlestick')
        self.weapon.add("Candlestick", 'candlestick')
        self.weapon.add("Knife", 'knife')
        self.weapon.add("Lead Pipe", 'lead')
        self.weapon.add("Revolver", 'revolver')
        self.weapon.add("Rope", 'rope')
        self.weapon.add("Wrench", 'wrench')
        
        self.container.add(self.weapon, 0, 75)
        
        self.accuse_btn = gui.Button("Make Accusation")
        self.accuse_btn.connect(gui.CLICK, self.close) 
        
        self.container.add(self.accuse_btn, 0,125)

    def start(self):
        gui.Dialog.__init__(self, self.title, self.container)
        self.open()
        
