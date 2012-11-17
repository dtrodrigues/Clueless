#!/usr/bin/env python

#

# global constants
FROM_SERVER = 0
TO_SERVER   = 1

START           = 0
ADD_PLAYER      = 1
NEXT_TURN       = 2
MADE_MOVE       = 3
MADE_SUGGESTION = 4
LOST_GAME       = 6
WON_GAME        = 7
WAS_DISPROVED   = 8

START_GAME      = 19
ADD_ME          = 20
MAKE_MOVE       = 21
MAKE_SUGGESTION = 22
MAKE_ACCUSATION = 23
DISPROVE        = 24

ERROR           = 99



class Message():

    def __init__(self,direction,typ,info=None,new_turn=False,comment=""):

        self.direction = direction
        self.typ       = typ
        self.info      = info
        self.new_turn  = new_turn
        # this won't necessarily be used, just for debugging
        self.comment   = comment

