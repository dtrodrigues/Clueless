#!/usr/local/bin/python

import pickle
import sys
import pygame
from pygame.locals import * 

import pgu
from pgu import gui, timer

import notebook, suggestion, accusation, board
import player, player_selection

from sector import Sector
import logic.message as m
import view.client

class DrawingArea(gui.Widget):
    def __init__(self, width, height):
        gui.Widget.__init__(self, width=width, height=height)
        self.imageBuffer = pygame.Surface((width, height))
        #self.imageBuffer = screen

    def paint(self, surf):
        # Paint whatever has been captured in the buffer
        surf.blit(self.imageBuffer, (0, 0))

    # Call this function to take a snapshot of whatever has been rendered
    # onto the display over this widget.
    def save_background(self):
        disp = pygame.display.get_surface()
        self.imageBuffer.blit(disp, self.get_abs_rect())


class MainGui(gui.Desktop):

    gameArea = None
    buttonArea = None
    messageArea = None
    # The game engine
    engine = None

    def __init__(self, disp):
        self.gameAreaHeight = 660
        self.gameAreaWidth = 660
        self.buttonAreaHeight = disp.get_height()
        self.buttonAreaWidth = disp.get_width() - self.gameAreaWidth
        self.messageAreaHeight = disp.get_height() - self.gameAreaHeight
        self.messageAreaWidth = self.gameAreaWidth
        self.gameArea = None
        self.buttonArea = None
        self.messageArea = None

        self.nb = notebook.Notebook()
        self.suggest = suggestion.Suggestion()
        self.accuse = accusation.Accusation()

        self.char = None
#       self.gameScreen = screen

	self.accusePressed = False
        self.suggestPressed = False
        self.endPressed = False

        gui.Desktop.__init__(self)

        # Setup the 'game' area where the action takes place
        self.gameArea = DrawingArea(height = self.gameAreaHeight,
                         width = self.gameAreaWidth )
        self.gameAreaRect = pygame.Rect(0,0,self.gameAreaHeight, self.gameAreaWidth)

        # Setup the button area
        self.buttonArea = gui.Container(
                          height=self.buttonAreaHeight, 
                          width=self.buttonAreaWidth)

        # Setup the message area
        self.messageArea = gui.Container(
                           height=self.messageAreaHeight, 
                           width=self.messageAreaWidth)

        self.setupButtons()
        self.setupMessage()
        #self.setupGame()

        tbl = gui.Container(height=disp.get_height(), width=disp.get_width())
        tbl.add(self.gameArea, 0,0)
        tbl.add(self.buttonArea, self.gameAreaWidth, 0)
        tbl.add(self.messageArea, 0, self.gameAreaHeight)


        self.init(tbl, disp)

    def setupGame(self):
        #self.myBoard = board.Board(self.gameArea.imageBuffer)
        #self.myBoard.showMap()
        self.char.update()

    def setupMessage(self):
        msg_label = gui.Label("Messages")
        self.msg_count = 0
        self.msg_box = gui.List(height=self.messageAreaHeight-40, width=self.messageAreaWidth)
        self.messageArea.add(msg_label, 0,0)
        self.messageArea.add(self.msg_box,0,20)

    def setupButtons(self):

        btn_tbl = gui.Table(height=self.buttonAreaHeight-250, width=self.buttonAreaWidth-20)

        def showNotebook():
            self.char.notebook.start()

        def showSuggest():
            #self.makeSuggestion()
            self.suggestPressed = True
            print("Suggestion requested.")

        def showAccuse():
            #self.makeAccusation()
            self.accusePressed = True

        def endTurn():
            #self.endTurn()
            self.endPressed = True

        def viewCards():
            self.char.view_cards()

        btn_tbl.tr()
        btn_notebook = gui.Button("View Notebook", height=20)
        btn_notebook.connect(gui.CLICK, showNotebook)
        btn_tbl.td(btn_notebook)

        btn_tbl.tr()
        btn_cards = gui.Button("View Cards", height=20)
        btn_cards.connect(gui.CLICK, viewCards)
        btn_tbl.td(btn_cards)

        btn_tbl.tr()
        btn_suggest = gui.Button("Suggest", height=20)
        btn_suggest.connect(gui.CLICK, showSuggest)
        btn_tbl.td(btn_suggest)

        btn_tbl.tr()
        btn_accuse = gui.Button("Accuse", height=20)
        btn_accuse.connect(gui.CLICK, showAccuse)
        btn_tbl.td(btn_accuse)

        btn_tbl.tr()
        btn_end = gui.Button("End Turn", height=20)
        btn_end.connect(gui.CLICK, endTurn)
        btn_tbl.td(btn_end)

        btn_tbl.tr()
        btn_quit = gui.Button("Quit", height=20)
        btn_quit.connect(gui.CLICK, self.quit)
        btn_tbl.td(btn_quit)


        self.buttonArea.add(btn_tbl,10,10)

	playerLabel = gui.Label("Players")
        self.player_list = gui.List(self.buttonAreaWidth-20, 100)
        self.player_count = 0
        self.buttonArea.add(playerLabel, 10,self.buttonAreaHeight-140)
        self.buttonArea.add(self.player_list, 10, self.buttonAreaHeight-120)
        
    def get_render_area(self):
        return self.gameArea.get_abs_rect()
        
class ClueGui():
    def __init__(self):
        pass

    def make_suggestion(self):
        succ, room, suspect, weapon = self.char.make_suggestion()
        if succ:
            d = m.Message(m.TO_SERVER, m.MAKE_SUGGESTION,
                    info={"suspect": view.client.guiToServ[self.char.name], "suggestion": tuple([room] + map(lambda x: view.client.guiToServ[x],[suspect, weapon]))})
            self.client.connection.sendLine(pickle.dumps(d))
    

    def make_accusation(self):
        suspect, weapon, room = self.char.make_accusation()

        d = m.Message(m.TO_SERVER, m.MAKE_ACCUSATION,
                info={"suspect": view.client.guiToServ[self.char.name], "accusation": tuple([room] + map(lambda x: view.client.guiToServ[x],[suspect, weapon]))})
        self.client.connection.sendLine(pickle.dumps(d))

    def endTurn(self):
        d = m.Message(m.TO_SERVER, m.END_TURN, info={'suspect': view.client.guiToServ[self.char.name]})
        self.client.connection.sendLine(pickle.dumps(d))

    def make_move(self, newx, newy):
        print("In make_move.")
        if self.char.move((newx, newy)):
            d = m.Message(m.TO_SERVER, m.MAKE_MOVE,info={'suspect': view.client.guiToServ[self.char.name], 'coord': (newx,newy)},comment="test")
            self.client.connection.sendLine(pickle.dumps(d))


    def initiate_game(self):

        valid_players = ['green', 'mustard', 'peacock', 'plum', 'scarlet', 'white']
        player_name = ''
        
        while player_name not in valid_players:
        
            p = player_selection.PlayerSelection(valid_players)
            p.start()
            player_name = p.p.value
            start_game = p.chk_start.value
            # Update valid_players with info from server
    
        #screen = pygame.Surface((660,660))        

        disp = pygame.display.set_mode((1000,800))
        self.app = MainGui(disp)
        self.app.engine = self
        self.app.char = player.Character(str(player_name), self.app.gameArea.imageBuffer)
        self.char = self.app.char
        self.char.update()
        self.app.update()

        self.count=0
        self.app.player_list.add(self.app.char.fancy_name)
        self.app.player_count += 1

        return start_game, player_name, self.char

    def start_playing(self):
        
        clock = pygame.time.Clock()

        while True:
            one_lap()
            clock.tick(60)
            
        sys.exit()


    def one_lap(self):

        while self.app.msg_count < len(self.app.char.messages):
            self.app.msg_box.add(self.app.char.messages[self.app.msg_count])
            self.app.msg_box.resize()
            self.app.msg_box.repaint()
            self.app.msg_count += 1

        if self.app.player_count < (len(self.app.char.opponents.keys())+1):
            for o in self.app.char.opponents.values():
                self.app.player_list.add(o.fancy_name)
                self.app.player_list.resize()
                self.app.player_list.repaint()
                self.app.player_count +=1

        self.char.update()
        self.app.update() 

        self.count += 1
        if self.count %10 == 0:
            print(self.app.char.fancy_name + " is in " + str(self.char.location.pos) + ".")
            
        GAMEOVER = False
        for event in pygame.event.get():
            worked = False
            if event.type == pygame.QUIT:
                GAMEOVER = True
                worked = True
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                newx, newy = self.char.location.x+1, self.char.location.y
                self.make_move(newx, newy)
            elif event.type == KEYDOWN and event.key == K_LEFT:
                newx, newy = self.char.location.x-1, self.char.location.y
                self.make_move(newx, newy)
            elif event.type == KEYDOWN and event.key == K_UP:
                newx, newy = self.char.location.x, self.char.location.y-1
                self.make_move(newx, newy)
            elif event.type == KEYDOWN and event.key == K_DOWN:
                newx, newy = self.char.location.x, self.char.location.y+1
                self.make_move(newx, newy)
            elif event.type == KEYDOWN and event.key == K_q:
                GAMEOVER = True
            elif event.type == KEYDOWN and event.key == K_p:
                if self.char.location.x == 0 and self.char.location.y == 0:
                    self.make_move(XMAX, YMAX)
                elif self.char.location.x == 0 and self.char.location.y == YMAX:
                    self.make_move(XMAX, 0)
                elif self.char.location.x == XMAX and self.char.location.y == 0:
                    self.make_move(0, YMAX)
                elif self.char.location.x == XMAX and self.char.location.y == YMAX:
                    self.make_move(0, 0)
            elif event.type == MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()

                for cell in self.char.board.cells:
                    if cell.clicked(mouse):
                        self.make_move(cell.x, cell.y)
                        worked = True
            if not worked:
                self.app.event(event)

        if self.app.suggestPressed:
            print("Found Suggestion Request")
            self.make_suggestion()
            self.app.suggestPressed = False
        if self.app.accusePressed:
            self.make_accusation()
            self.app.accusePressed = False
        if self.app.endPressed:
            self.endTurn()
            self.app.endPressed = False

        self.char.screen.blit( self.char.board.background, (0,0) )
        self.char.update()
        #self.app.gameArea.paint(self.app.char.screen)
        updates = self.app.update(self.app.screen)
        pygame.display.update(updates)
        pygame.time.wait(10)
        if GAMEOVER:
            from twisted.internet import reactor
            reactor.callFromThread(reactor.stop)

#class ClueGui():
#    def __init__(self):
#        disp = pygame.display.set_mode((1000,800))
#        self.app = MainGui(disp)
#        self.app.connect(gui.QUIT, self.app.quit, None)
#        self.app.run()


if __name__ == '__main__':
    disp = pygame.display.set_mode((1000, 800))

    app = MainGui(disp)
    app.connect(gui.QUIT,app.quit,None)
    app.run()
