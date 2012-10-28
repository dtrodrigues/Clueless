#!/usr/bin/env python
import random, datetime
import pickle as p

# define new exceptions here
class PlayerException(IOError): pass
class EmptyDeckError(AttributeError): pass
class NoSuchPlayerError(ValueError): pass
class InvalidMoveError(ValueError): pass
class GameOverError(ValueError): pass
class InvalidCoordError(ValueError): pass


# some global variables
scarlet = 0
mustard = 1
white   = 2
green   = 3
peacock = 4
plum    = 5

player_order = [scarlet,mustard,white,green,peacock,plum]

class game():

    def __init__(self,playerlist):
        self.board = board()
        self.deck = deck()
        self.playerlist = playerlist
        self.numplayers  = len(playerlist)
        self.current_player = self.playerlist[0]
        self.disproving_player = self.playerlist[1]

        if (self.numplayers < 2 or self.numplayers > 6):
            raise PlayerException("Attempted to initialize game with %d \
players. Invalid number of players.",numplayers)

        self.solution_cards = self.deck.draw_solution_cards()

        self.turn_number = 0
        self.game_over   = False

    def distribute_remaining_cards(self):
        '''Randomly distrubutes the remaining cards in the deck among all \
players.'''
        all_cards = self.deck.return_all_shuffled()
        num_cards = len(all_cards)

        for x in range(num_cards):
            self.playerlist[x % self.numplayers].add_card(all_cards[x])

        return True

    def next_turn(self):
        '''Advances the state of the game to the next turn. Raises an \
exception if the game is over. Returns True on success.'''

        if self.game_over:
            raise GameOverError("Cannot make new move: game is already over.")

        self.turn_number += 1 
        self.current_player = self.playerlist[self.turn_number %
self.numplayers]
        self.disproving_player = self.playerlist[(self.turn_number+1) %
self.numplayers]

        return True

    def update_player_position(self,player,coordinate):
        '''Updates the position of the player on the board with the given \
coordinate. Returns True on success, False otherwise.'''

        # give it a try, return false if it doesn't work
        try:
            self.board.update_player_position(player,coordinate)
            return True 

        except InvalidMoveError, errmsg:
            return False

    def return_board(self):
        pass

    def __check_accusation(self,suggestion):
        '''Returns True if the suggestion is correct, False otherwise.'''
        if suggestion == self.solution_cards:
            return True
        else:
            return False

    def check_suggestion(self):
        return True

    # moves the suspect being accused to the room proposed
    def __move_player_for_suggestion(self,player):
        '''Moves the suggested or accused suspect to the room proposed by \
        suggesting or accusing player. Returns True if successful.'''
        return True

    def __correct_room_for_suggestion(self,player):
        '''Checks that the suggesting player is in the room before allowing an \
        accusation or suggestion to be made. Returns True if condition is met, 
        False otherwise.'''
        return True

    def declare_loser(self):
        return True

    def declare_winner(self):
        return True

    def end_game(self):
        self.game_over = True
        return True



class player():

    def __init__(self,name,suspect,ip_address):
        self.connected = True
        self.name = name
        self.cards = []
        self.loser = False
        self.ip_address = ip_address

    def who_am_i(self):
        return (name,suspect,ip_address)

    def add_card(self,card):
        self.cards += [card]
        return card

    def where_am_i(self):
        return True

    def make_move(self):
        pass

    def make_suggestion(self,suspect,weapon,room):
        pass

    def make_accusation(self,suspect,weapon,room):
        pass

    def can_disprove(self,suspect,weapon,room):
        return True

    def lose_game(self):
        self.loser= True


class deck():

    def __init__(self):
        # hopefully this will do for our purposes
        random.seed(datetime.datetime.now()) 

        self.rooms = ['Study','Hall','Lounge','Library','Billiard Room','Dining \
Room','Conservatory','Ballroom','Kitchen']
        self.suspects = ['Miss Scarlet','Colonel Mustard','Mrs. White','Mr. \
Green','Mrs. Peacock','Professor Plum']
        self.weapons = ['Candlestick','Dagger','Lead Pipe','Revolver','Rope','Wrench']

        random.shuffle(self.rooms)
        random.shuffle(self.suspects)
        random.shuffle(self.weapons)

    def draw_solution_cards(self):
        '''Returns three solution cards (room,suspect,weapon).'''
        if self.__deck_empty():
            raise EmptyDeckError()

        r = self.rooms.pop()
        s = self.suspects.pop()
        w = self.weapons.pop()

        return (r,s,w)

    def return_all_shuffled(self):
        '''Returns a list containing all cards currently in the deck, \
shuffled.'''
        if self.__deck_empty():
            return EmptyDeckError()

        all_cards = self.rooms + self.suspects + self.weapons
        random.shuffle(all_cards)

        return all_cards

    def __deck_empty(self):
        if len(self.rooms) + len(self.suspects) + len(self.weapons) == 0:
            return True
        else:
            return False

class coord():
    '''The entire purpose of this class is to make it impossible to define an \
invalid coordinate.'''

    def __init__(self,x,y):
        self.min_xy = 0
        self.max_xy = 4
        self.invalid_coords = [(1,1),(1,3),(3,1),(3,3)]

        if x < self.min_xy:
            raise InvalidCoordError("X value less than minimum x value of 0.")
        if x > self.max_xy:
            raise InvalidCoordError("X value greater than max x value of 4.")
        if y < self.min_xy:
            raise InvalidCoordError("Y value less than minimum y value of 0.")
        if y > self.max_xy:
            raise InvalidCoordError("Y value greater than max y value of 4.")
        if (x,y) in self.invalid_coords:
            raise InvalidCoordError("Coordinate given is not a valid position \
on the board.")

        self.x = x
        self.y = y

    def return_tuple(self):
        return (x,y)

class board():

    def __init__(self):
        self.min_xy = 0
        self.max_xy = 4
        # if players are in a position, then the player reference will be at
        # that coordinate, otherwise the value at that coordinate will be zero
        self.board  = [[0 for x in range(5)] for y in range(5)] 
        self.not_spaces = [(1,1),(1,3),(3,1),(3,3)]
        self.rooms = {(0,0):"Study",
                      (0,2):"Hall",
                      (0,4):"Lounge",
                      (2,0):"Library",
                      (2,2):"Billiard Room",
                      (2,4):"Dining Room",
                      (4,0):"Conservatory",
                      (4,2):"Ballroom",
                      (4,4):"Kitchen" 
                     } 

        # this will reflect the start positions of each player to begin with
        self.player_positions = {"Miss Scarlet":(0,3),
                                 "Colonel Mustard":(1,4),
                                 "Mrs. White":(4,3),
                                 "Mr. Green":(4,1),
                                 "Mrs. Peacock":(3,0),
                                 "Professor Plum":(1,0)
                                }

    def find_player(self,player):
        for x in self.player_positions.keys():
            if x == player:
                return self.player_positions[x]

        # error if you get to here
        raise NoSuchPlayerError()

    def update_player_position(self,player,coordinate):
        '''Given a player and a coordinate, returns True if the position can \
be updated and raises InvalidMoveError otherwise. Updates the board accordingly.'''
        # raise an exception if not a valid player
        # raise exception if not a valid coordinate
        # raise exception if not a valid move
        if not self.__validate_move(player,coordinate):
            raise InvalidMoveError

        # if you get here, success, so update the coordinate
        self.player_positions[player] = coordinate
        return True

    def __position_is_empty(self,coordinate):
        '''Given a coordinate, returns True if position is empty and \
        False if position is occupied by another player.'''

        if self.board[position[0]][position[1]] == 0:
            return True
        else:
            return False

    def __validate_move(self,player,coordinate):
        '''Given a player and a coordinate, determines whether the \
proposed move is allowable or not. Returns True if allowable, False if \
otherwise.'''
        # this means someone is already there, so can't move there
        if not self.__position_is_empty(coordinate):
            return False
        # this means it's not actually a space, so can't move there either
        if coordinate in self.not_spaces:
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
        self.__valid_coordinate(coord)

        if coord in self.rooms.keys():
            return self.rooms[coord]

        elif coord in self.not_spaces:
            return "Not a valid space."

        else:
            return "Hallway"

    def __valid_coordinate(self,coord):
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
