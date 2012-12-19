#!/usr/bin/env python

import pygame, sys
from pgu import gui

class Suggestion(gui.Dialog):
    def __init__(self):

        self.title = gui.Label("Make a Suggestion")
        self.sgt_table = gui.Container(width=100, height=150)
        self.label = gui.Label("Suggest a suspect, room, and weapon.")
        self.sgt_table.add(self.label, 0,0)

        self.suspect = gui.Select(value = 'green')
        self.suspect.add("Mr. Green", 'green')
        self.suspect.add("Colonel Mustard", 'mustard')
        self.suspect.add("Mrs. Peacock", 'peacock')
        self.suspect.add("Professor Plum", 'plum')
        self.suspect.add("Miss Scarlet", 'scarlet')
        self.suspect.add("Mrs. White", 'white')
       
        self.sgt_table.add(self.suspect,0,25)
        
        self.room = gui.Select(value = "Ballroom")
        self.room.add("Ballroom", "Ballroom")
       
        self.sgt_table.add(self.room,0,50)
        
        self.weapon = gui.Select(value = 'candlestick')
        self.weapon.add("Candlestick", 'candlestick')
        self.weapon.add("Knife", 'knife')
        self.weapon.add("Lead Pipe", 'lead_pipe')
        self.weapon.add("Revolver", 'revolver')
        self.weapon.add("Rope", 'rope')
        self.weapon.add("Wrench", 'wrench')
       
        self.sgt_table.add(self.weapon,0,75)
        
        self.suggest_btn = gui.Button("Make Suggestion")
        self.suggest_btn.connect(gui.CLICK, self.close) 
       
        self.sgt_table.add(self.suggest_btn,0,125)


    def create(self, room):
        self.sgt_table.remove(self.room)
        self.room = gui.Select(value = room)
        self.room.add(room,room)
        self.sgt_table.add(self.room,0,50) 

        gui.Dialog.__init__(self, self.title, self.sgt_table)
        self.open()

        
