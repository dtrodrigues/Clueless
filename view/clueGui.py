import pygame, sys
from pygame.locals import *
import pickle

from pgu import gui

import board, notebook, player_selection, suggestion, accusation, card, disprove, player
import gamerunner
from sector import Sector
import logic.message as m
import view.client

class ClueGUI:

    def __init__(self):
        pass

    def initiate_game(self):

        valid_players = ['green', 'mustard', 'peacock', 'plum', 'scarlet', 'white']
        player_name = ''
        
        while player_name not in valid_players:
        
            p = player_selection.PlayerSelection(valid_players)
            p.start()
            player_name = p.p.value
            start_game = p.chk_start.value
            # Update valid_players with info from server
            
        self.char = player.Character(str(player_name))
        return start_game, player_name, self.char
        #start_playing(player)

    def start_playing(self):
        
        clock = pygame.time.Clock()

        while True:
            one_lap()
            clock.tick(120)
            
        sys.exit()

    def make_move(self, newx, newy):
        if self.char.move((newx, newy)):
            d = m.Message(m.TO_SERVER, m.MAKE_MOVE,info={'suspect': view.client.guiToServ[self.char.name], 'coord': (newx,newy)},comment="test")
            self.client.connection.sendLine(pickle.dumps(d))

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

            
    def end_turn(self):
        d = m.Message(m.TO_SERVER, m.END_TURN, info={'suspect': view.client.guiToServ[self.char.name]})
        self.client.connection.sendLine(pickle.dumps(d))

    def one_lap(self):        
            
        GAMEOVER = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAMEOVER = True
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
                if self.char.board.btn_exit.pressed(mouse):        # Exit game
                    GAMEOVER = True
                if self.char.board.btn_notebook.pressed(mouse): # View Notebook
                    self.char.notebook.start()
                if self.char.board.btn_suggest.pressed(mouse): # Make a Suggestion
                    self.make_suggestion()
                    #self.char.make_suggestion()
                if self.char.board.btn_accuse.pressed(mouse): # Make an Accusation
                    self.make_accusation()
                    #self.char.make_accusation()
                if self.char.board.btn_cards.pressed(mouse):
                    self.char.view_cards()
                if self.char.board.btn_end.pressed(mouse): # End Turn
                    self.end_turn() 

                for cell in self.char.board.cells:
                    if cell.clicked(mouse):
                        self.make_move(cell.x, cell.y)

        self.char.screen.blit( self.char.board.background, (0,0) )
        self.char.update()
        pygame.display.flip()
        if GAMEOVER:
            from twisted.internet import reactor
            reactor.callFromThread(reactor.stop)


if __name__ == '__main__':
    print "don't run as main. use ./run-client"
