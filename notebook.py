#!/usr/bin/env python

import pygame, sys
from pgu import gui

class Notebook():
    def __init__(self, screen = None):

        self.screen = screen
        self.WIDTH = 400
        self.HEIGHT = 640

        self.app = gui.Desktop()

        self.app.connect(gui.QUIT, self.app.quit, None)

        self.c = gui.Table(width=400, height=640)
        
        self.green_val = 'u'
        self.mustard_val = 'u'
        self.peacock_val = 'u'
        self.plum_val = 'u'
        self.scarlet_val = 'u'
        self.white_val = 'u'
        
        self.ballroom_val = 'u'
        self.billiard_val = 'u'
        self.conservatory_val = 'u'
        self.dining_val = 'u'
        self.hall_val = 'u'
        self.kitchen_val = 'u'
        self.library_val = 'u'
        self.lounge_val = 'u'
        self.study_val = 'u'
    
        self.candlestick_val = 'u'
        self.knife_val = 'u'
        self.lead_val = 'u'
        self.revolver_val = 'u'
        self.rope_val = 'u'
        self.wrench_val = 'u'
        
#        self.app.run(self.c)

        self.display_notebook()

    def display_notebook(self):
        
        self.c.tr()
        self.c.td(gui.Label("Detective's Notebook"), colspan=4)

        self.c.tr()
        self.c.td(gui.Label("Suspect"))
        self.c.td(gui.Label("No"))
        self.c.td(gui.Label("Yes"))
        self.c.td(gui.Label("Unknown"))

        self.c.tr()
        self.c.td(gui.Label("Mr. Green"))

        self.green = gui.Group(name="green", value=self.green_val)
        self.c.td(gui.Radio(self.green,value='y'))
        self.c.td(gui.Radio(self.green,value='n'))
        self.c.td(gui.Radio(self.green,value='u'))

        self.c.tr()
        self.c.td(gui.Label("Cln. Mustard"))

        self.mustard = gui.Group(name='mustard', value=self.mustard_val)
        self.c.td(gui.Radio(self.mustard,value='y'))
        self.c.td(gui.Radio(self.mustard,value='n'))
        self.c.td(gui.Radio(self.mustard,value='u'))

        self.c.tr()
        self.c.td(gui.Label("Mrs. Peacock"))

        self.peacock_grp = gui.Group(name='peacock', value=self.peacock_val)
        self.c.td(gui.Radio(self.peacock_grp,value='y'))
        self.c.td(gui.Radio(self.peacock_grp,value='n'))
        self.c.td(gui.Radio(self.peacock_grp,value='u'))

        self.c.tr()
        self.c.td(gui.Label("Prof. Plum"))

        self.plum_grp = gui.Group(name='plum', value=self.plum_val)
        self.c.td(gui.Radio(self.plum_grp,value='y'))
        self.c.td(gui.Radio(self.plum_grp,value='n'))
        self.c.td(gui.Radio(self.plum_grp,value='u'))

        self.c.tr()
        self.c.td(gui.Label("Miss Scarlet"))

        self.scarlet_grp = gui.Group(name='scarlet', value=self.scarlet_val)
        self.c.td(gui.Radio(self.scarlet_grp,value='y'))
        self.c.td(gui.Radio(self.scarlet_grp,value='n'))
        self.c.td(gui.Radio(self.scarlet_grp,value='u'))

        self.c.tr()
        self.c.td(gui.Label("Ms. White"))

        self.white_grp = gui.Group(name='white',value=self.white_val)
        self.c.td(gui.Radio(self.white_grp,value='y'))
        self.c.td(gui.Radio(self.white_grp,value='n'))
        self.c.td(gui.Radio(self.white_grp,value='u'))

        self.c.tr()
        self.c.td(gui.Label("Rooms"))

        self.c.tr()
        self.c.td(gui.Label("Ballroom"))

        self.ballroom_grp = gui.Group(name='ballroom', value=self.ballroom_val)
        self.c.td(gui.Radio(self.ballroom_grp, value='y'))
        self.c.td(gui.Radio(self.ballroom_grp, value='n'))
        self.c.td(gui.Radio(self.ballroom_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Billiard Room"))

        self.billiard_grp = gui.Group(name='billiard_room', value=self.billiard_val)
        self.c.td(gui.Radio(self.billiard_grp, value='y'))
        self.c.td(gui.Radio(self.billiard_grp, value='n'))
        self.c.td(gui.Radio(self.billiard_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Conservatory"))

        self.conservatory_grp = gui.Group(name='conservatory', value=self.conservatory_val)
        self.c.td(gui.Radio(self.conservatory_grp, value='y'))
        self.c.td(gui.Radio(self.conservatory_grp, value='n'))
        self.c.td(gui.Radio(self.conservatory_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Dining Room"))

        self.dining_grp = gui.Group(name='dining', value=self.dining_val)
        self.c.td(gui.Radio(self.dining_grp, value='y'))
        self.c.td(gui.Radio(self.dining_grp, value='n'))
        self.c.td(gui.Radio(self.dining_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Hall"))

        self.hall_grp = gui.Group(name='hall', value=self.hall_val)
        self.c.td(gui.Radio(self.hall_grp, value='y'))
        self.c.td(gui.Radio(self.hall_grp, value='n'))
        self.c.td(gui.Radio(self.hall_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Library"))

        self.library_grp = gui.Group(name='library', value=self.library_val)
        self.c.td(gui.Radio(self.library_grp, value='y'))
        self.c.td(gui.Radio(self.library_grp, value='n'))
        self.c.td(gui.Radio(self.library_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Lounge"))

        self.lounge_grp = gui.Group(name='lounge', value=self.lounge_val)
        self.c.td(gui.Radio(self.lounge_grp, value='y'))
        self.c.td(gui.Radio(self.lounge_grp, value='n'))
        self.c.td(gui.Radio(self.lounge_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Kitchen"))

        self.kitchen_grp = gui.Group(name='kitchen', value=self.kitchen_val)
        self.c.td(gui.Radio(self.kitchen_grp, value='y'))
        self.c.td(gui.Radio(self.kitchen_grp, value='n'))
        self.c.td(gui.Radio(self.kitchen_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Study"))

        self.study_grp = gui.Group(name='study', value=self.scarlet_val)
        self.c.td(gui.Radio(self.study_grp, value='y'))
        self.c.td(gui.Radio(self.study_grp, value='n'))
        self.c.td(gui.Radio(self.study_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Weapons"))

        self.c.tr()
        self.c.td(gui.Label("Candlestick"))

        self.candle_grp = gui.Group(name='candle', value=self.candlestick_val)
        self.c.td(gui.Radio(self.candle_grp, value='y'))
        self.c.td(gui.Radio(self.candle_grp, value='n'))
        self.c.td(gui.Radio(self.candle_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Knife"))

        self.knife_grp = gui.Group(name='knife', value=self.knife_val)
        self.c.td(gui.Radio(self.knife_grp, value='y'))
        self.c.td(gui.Radio(self.knife_grp, value='n'))
        self.c.td(gui.Radio(self.knife_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Lead Pipe"))

        self.lead_grp = gui.Group(name='lead', value=self.lead_val)
        self.c.td(gui.Radio(self.lead_grp, value='y'))
        self.c.td(gui.Radio(self.lead_grp, value='n'))
        self.c.td(gui.Radio(self.lead_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Revolver"))

        self.revolver_grp = gui.Group(name='revolver', value=self.revolver_val)
        self.c.td(gui.Radio(self.revolver_grp, value='y'))
        self.c.td(gui.Radio(self.revolver_grp, value='n'))
        self.c.td(gui.Radio(self.revolver_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Rope"))

        self.rope_grp = gui.Group(name='rope', value=self.rope_val)
        self.c.td(gui.Radio(self.rope_grp, value='y'))
        self.c.td(gui.Radio(self.rope_grp, value='n'))
        self.c.td(gui.Radio(self.rope_grp, value='u'))

        self.c.tr()
        self.c.td(gui.Label("Wrench"))

        self.wrench_grp = gui.Group(name='wrench', value=self.wrench_val)
        self.c.td(gui.Radio(self.wrench_grp, value='y'))
        self.c.td(gui.Radio(self.wrench_grp, value='n'))
        self.c.td(gui.Radio(self.wrench_grp, value='u'))

        self.exit_btn = gui.Button("Exit")
        self.exit_btn.connect(gui.CLICK, self.app.quit, None) 

        self.c.tr()
        self.c.td(self.exit_btn)

    def start(self):
        
        self.app.run(self.c)
    
notebook = Notebook()
notebook.start()
