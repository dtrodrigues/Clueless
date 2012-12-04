#!/usr/bin/env python
import random, datetime
import pickle

# define new exceptions here
class PlayerError(IOError): pass
class NotReadyError(AttributeError): pass
class PlayerCollisionError(IOError): pass
class EmptyDeckError(AttributeError): pass
class NoSuchPlayerError(ValueError): pass
class InvalidMoveError(ValueError): pass
class GameOverError(ValueError): pass
class InvalidCoordError(ValueError): pass

__MIN_PLAYERS__ = 2
__MAX_PLAYERS__ = 6

__rooms__ = ['Study','Hall','Lounge','Library','Billiard Room','Dining Room',
'Conservatory','Ballroom','Kitchen']
__suspects__ = ['Miss Scarlet','Colonel Mustard','Mrs. White','Mr. Green','Mrs. Peacock', 'Professor Plum']
__weapons__ = ['Candlestick','Dagger','Lead Pipe','Revolver','Rope','Wrench']



###################################################################
#
#   CLASS: game
#
#
###################################################################

class Game():

#
#   INIT
#
    def __init__(self):
        self.board = Board()
        self.deck = Deck()

        # the hash values will be populated with player objects
        # as players are added, but for now they are empty
        self.players = {x:"" for x in __suspects__}
        self.playerlist = [] # this will make it easier to deal cards
        self.available_suspects = [x for x in __suspects__]

        self.numplayers  = 0
        self.current_player = ""
        self.losers = []

        self.solution_cards = self.deck.draw_solution_cards()

        self.ready_to_start = False
        self.turn_number = 0
        self.game_over   = False

#
#   ADD PLAYER
#
    def add_player(self,player):

        if self.numplayers == 6:
            raise PlayerError("Game already hosting six players. No additional \
players allowed.")

        if player.suspect not in __suspects__:
            raise PlayerError("Unknown suspect chosen. Add player failed.")
        if self.players[player.suspect]:
            raise PlayerError("This suspect already taken by another player.")

        self.players[player.suspect] = player
        self.playerlist = self.players_in_order()
        self.available_suspects.remove(player.suspect)
        self.numplayers += 1

        if self.numplayers > 1:
            self.ready_to_start = True
            self.current_player = self.playerlist[0].suspect

        return self.ready_to_start

#
#   PLAYERS IN ORDER
#
    def players_in_order(self):

        plist = []
        for x in __suspects__:
            if self.players[x]:
                plist += [self.players[x]]

        return plist

    def distribute_remaining_cards(self):
        '''Randomly distrubutes the remaining cards in the deck among all \
players.'''
        all_cards = self.deck.return_all_shuffled()
        num_cards = len(all_cards)

        for x in range(num_cards):
            self.playerlist[x % self.numplayers].add_card(all_cards[x])

        return True


#
#   NEXT TURN
#
    def next_turn(self):
        '''Advances the state of the game to the next turn. Raises an \
exception if the game is over. Returns True on success.'''

        if self.game_over:
            raise GameOverError("Cannot make new move: game is already over.")

        # this needs to account for the possibility that a player has already
        # lost
        self.next_player()
        self.turn_number += 1

        # return the new suspect
        return self.current_player



    def next_player(self):

        if len(self.losers) >= self.numplayers -1:
            return False 

        current = 0
        for x in range(self.numplayers):
            if self.playerlist[x].suspect == self.current_player:
                current = x
                break

        x = 0
        while(x < self.numplayers-1):

            current = (current + 1) % self.numplayers
            if self.playerlist[current].suspect in self.losers:
                x += 1
                continue

            else:
                self.current_player = self.playerlist[current].suspect
                return self.current_player

        return False


    def who_can_disprove(self,suggestion):
        """ returns a 3-tuple of the player who can disprove the suggestion (or False),
        the cards they can use to disprove the suggestion (or None), and a list of players
        who can't disprove the suggestion"""

        #print "player list is " + str(self.playerlist)

        current = 0
        for x in range(self.numplayers):
            #print "for iter"
            if self.playerlist[x].suspect == self.current_player:
                current = x
                #print str(current) + " is current"
                break


        canDisprove = False
        disproveCards = []
        whoCantDisprove = []

        # we care about all players except the suggester
        for x in range(self.numplayers - 1):

            current = (current + 1) % self.numplayers
            #print "current in loop is " + str(current)
            for card in self.playerlist[current].cards:
                if card in suggestion:
                    canDisprove = True
                    disproveCards += [card]
                    disprover = self.playerlist[current].suspect
                    #print "disprover is " +  disprover

            if canDisprove:
                #print disprover, disproveCards, whoCantDisprove
                return disprover, disproveCards, whoCantDisprove
            else:
                whoCantDisprove += [self.playerlist[current].suspect]



        # no one can disprove
        #print whoCantDisprove
        return False, disproveCards, whoCantDisprove

#
#   UPDATE PLAYER POSITION
#
    def update_player_position(self,player,coordinate):
        '''Updates the position of the player on the board with the given \
coordinate. Returns True on success, False otherwise.'''

        # give it a try, return false if it doesn't work
        try:
            self.board.update_player_position(player,coordinate)
            return True 

        except InvalidMoveError, errmsg:
            return False


#
#   PICKLE BOARD
#
    def pickle_board(self):
        '''Returns the board as a Pickle.'''
        return pickle.dumps(self.board)

#
#   CHECK SUGGESTION
#
    def check_suggestion(self,suggestion):

        room = suggestion[0]
        suspect = suggestion[1]
        weapon = suggestion[2]

        # move suspected player to the correct room
        self.board.move_player_to_room(suspect,room)
        self.board.move_weapon_to_room(weapon,room)

        return self.who_can_disprove(suggestion)



#
#   CHECK ACCUSATION
#
    def check_accusation(self,accusation):
        '''Returns True if the suggestion is correct, False otherwise.'''

        room = accusation[0]
        suspect = accusation[1]
        weapon = accusation[2]

        # move the accused suspect to the correct room
        self.board.move_player_to_room(suspect,room)
        self.board.move_weapon_to_room(suspect,room)

        if suggestion == self.solution_cards:
            return True
        else:
            return False

#
#   CORRECT ROOM FOR SUGGESTION OR ACCUSATION
#
    def correct_room_for_suggestion(self,player):
        '''Checks that the suggesting player is in the room before allowing an 
        accusation or suggestion to be made. Returns True if condition is met, 
        False otherwise.'''
        return True

#
#   DECLARE LOSER
#
    def declare_loser(self,suspect):
        self.losers += [suspect]
        return True

#
#   DECLARE WINNER
#
    def declare_winner(self):
        return True


#
#   END GAME
#
    def end_game(self):
        self.game_over = True
        return True

##############################################################
#
#   CLASS: player
#
#
##############################################################

class Player():

    def __init__(self,name,suspect,ip_address=None,port=None):
        self.connected = True
        self.name = name
        if suspect not in __suspects__:
            raise PlayerError("Invalid suspect.")

        self.suspect = suspect
        self.cards = []
        self.loser = False
        self.ip_address = ip_address
        self.port = port
        self.current_position = ""

    def who_am_i(self):
        return (self.name,self.suspect,self.ip_address)

    def add_card(self,card):
        self.cards += [card]
        return card

    def can_disprove(self,suspect,weapon,room):

        if suspect in self.cards:
            return True
        elif weapon in self.cards:
            return True
        elif room in self.cards:
            return True
        else:
            return False

    def lose_game(self):
        self.loser= True

    def __repr__(self):
        return '< %s -- %s -- %s >' % (self.name,self.suspect,self.ip_address)

################################################################
#
#   CLASS: deck
#
#
################################################################

class Deck():

    def __init__(self):
        # hopefully this will do for our purposes
        random.seed(datetime.datetime.now()) 

        self.rooms = __rooms__
        self.suspects = [x for x in __suspects__]
        self.weapons = __weapons__
        random.shuffle(self.weapons)

    def draw_solution_cards(self):
        '''Returns three solution cards (room,suspect,weapon).'''
        if self.deck_empty():
            raise EmptyDeckError()

        r = self.rooms.pop()
        s = self.suspects.pop()
        w = self.weapons.pop()

        return (r,s,w)

    def return_all_shuffled(self):
        '''Returns a list containing all cards currently in the deck, \
shuffled.'''
        if self.deck_empty():
            return EmptyDeckError()

        all_cards = self.rooms + self.suspects + self.weapons
        random.shuffle(all_cards)

        return all_cards

    def deck_empty(self):
        if len(self.rooms) + len(self.suspects) + len(self.weapons) == 0:
            return True
        else:
            return False

##################################################################
#
#   CLASS: board
#
#
##################################################################

class Board():

    def __init__(self):
        self.min_xy = 0
        self.max_xy = 4
        # if players are in a position, then the player reference will be at
        # that coordinate, otherwise the value at that coordinate will be zero
        self.board  = [[0 for x in range(5)] for y in range(5)] 
        self.not_spaces = [(1,1),(1,3),(3,1),(3,3)]
        self.rooms = {(0,0):"Study",
                      (0,2):"Library",
                      (0,4):"Conservatory",
                      (2,0):"Hall",
                      (2,2):"Billiard Room",
                      (2,4):"Ballroom",
                      (4,0):"Lounge",
                      (4,2):"Dining Room",
                      (4,4):"Kitchen" 
                     } 

        # this will reflect the start positions of each player to begin with
        self.player_positions = {"Miss Scarlet":(3,0),
                                 "Colonel Mustard":(4,1),
                                 "Mrs. White":(3,4),
                                 "Mr. Green":(1,4),
                                 "Mrs. Peacock":(0,3),
                                 "Professor Plum":(0,1)
                                }

        # and this reflects the start position of each weapon
        self.weapon_positions = {"Candlestick":(0,0)
                                 "Dagger":(0,2)
                                 "Lead Pipe":(0,4)
                                 "Rope":(2,0)
                                 "Revolver":(4,0)
                                 "Wrench":(4,2)
                                }

    def find_player(self,suspect):
        for x in self.player_positions.keys():
            if x == suspect:
                return self.player_positions[x]

        # error if you get to here
        raise NoSuchPlayerError()


    def available_moves(self,suspect):

        x,y = self.find_player(suspect)
        candidates = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]

        # what if there's a secret passage?
        if (x,y) == (0,0):
            candidates += [(4,4)]
        if (x,y) == (4,4):
            candidates += [(0,0)]
        if (x,y) == (4,0):
            candidates += [(0,4)]
        if (x,y) == (0,4):
            candidates += [(4,0)]


        available = []

        for i in candidates:

            occupied = False

            # make sure the coordinate is on the board
            if (i[0] > self.max_xy) or (i[1] > self.max_xy):
                continue
            if (i[0] < self.min_xy) or (i[1] < self.min_xy):
                continue

            # make sure it's actually a space
            if i in self.not_spaces:
                continue

            # make sure that space isn't occupied if it's a hallway (not a
            # room)
            if not self.rooms.has_key(i)
                for key in self.player_positions.keys():
                    if self.player_positions[key] == i:
                        occupied = True
                        break

            if occupied:
                continue

            # otherwise, I guess it's a good space
            available += [i]

        return available


    def update_player_position(self,player,coordinate):
        '''Given a player and a coordinate, returns True if the position can \
be updated and raises InvalidMoveError otherwise. Updates the board accordingly.'''
        # raise an exception if not a valid player
        # raise exception if not a valid coordinate
        # raise exception if not a valid move
        if not self.validate_move(player,coordinate):
            raise InvalidMoveError

        # if you get here, success, so update the coordinate
        self.player_positions[player] = coordinate
        return True



    def move_player_to_room(self,player,room):
        '''This should only be used for accusations and suggestions.'''

        coord = ()
        for x in self.rooms.keys():
            if self.rooms[x] == room:
                self.player_positions[player] = x
                return True

        # if you get here, it's not a room
        return False


    def move_weapon_to_room(self,weapon,room)

        coord = ()
        for x in self.rooms.keys():
            if self.rooms[x] == room:
                self.weapon_positions[weapon] = x
                return True

        # if you get here, it's not a weapon
        return False



    def position_is_empty(self,coordinate):
        '''Given a coordinate, returns True if position is empty and \
        False if position is occupied by another player.'''

        if self.board[coordinate[0]][coordinate[1]] == 0:
            return True
        else:
            return False



    def validate_move(self,player,coordinate):
        '''Given a player and a coordinate, determines whether the \
proposed move is allowable or not. Returns True if allowable, False if \
otherwise.'''
        # this means it's not actually a space, so can't move there either
        if coordinate in self.not_spaces:
            return False
        # if it's a room, there can be more than one person
        # otherwise, it better be empty
        if coordinate not in self.rooms.keys():
            if not self.position_is_empty(coordinate):
                return False

        current_coord = self.player_positions[player]

        delta_x = abs(current_coord[0] - coordinate[0])
        delta_y = abs(current_coord[1] - coordinate[1])

        # make sure that the proposed move is only one space away
        if delta_x > 1:
            return False
        if delta_y > 1:
            return False
        # make sure the proposed move is not at a diagonal
        if delta_x + delta_y != 1:
            return False

        # if you make it here, it's a valid move
        self.player_positions[player] = coordinate 
        return True



    def room_name(self, coord):
        self.valid_coordinate(coord)

        if coord in self.rooms.keys():
            return self.rooms[coord]

        elif coord in self.not_spaces:
            return "Not a valid space."

        else:
            return "Hallway"



    def valid_coordinate(self,coord):
        '''Private method. Checks that given coordinate is valid form.'''
        if type(coord) != tuple:
            raise ValueError("Invalid parameter provided: parameter must be valid coordinate (x,y)")

        if len(coord) != 2:
            raise ValueError("Invalid length tuple provided: parameter must be valid coordinate (x,y)")

        if coord[0] > self.max_xy or coord[0] < self.min_xy:
            raise ValueError("Invalid value for x coordinate. Must be between 0 and 4.")

        if coord[1] > self.max_xy or coord[1] < self.min_xy:
            raise ValueError("Invalid value for y coordinate. Must be between 0 and 4.")

        # if it's valid, return true
        return True



    def pickle(self):
        pickle = ""
        return pickle


def main():
    print("Nothing here for now")

if __name__ == "__main__":
    main()
