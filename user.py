import board
import client
import socket

class Character():
    def __init__(self, name):
        self.name = name
        self.location = get_starting_location()

    def get_starting_location(self):
        if self.name == 'green':
            location = Hallway_10
        elif self.name == 'mustard':
            location = Hallway_4
        elif self.name == 'peacock':
            location = Hallway_7
        elif self.name == 'plum':
            location = Hallway_2
        elif self.name == 'scarlet':
            location = Hallway_1
        else: # self.name == 'white'
            location = Hallway_11
        return location

class User():
    def __init__(self, name):
        self.player_number = 1
        self.character = Character(name)
        self.cards = []
        self.location = self.character.get_starting_location()
        
    def get_moves():
        movelist = ['Hallway 8', 'Hallway 10', 'Hallway 11']
        
class Suggestion():
    def __init__(self, room, suspect, weapon)
        self.room = room
        self.suspect = suspect
        self.weapon = weapon
        
        
class Accusation():
    def __init__(self, room, suspect, weapon)
        self.room = room
        self.suspect = suspect
        self.weapon = weapon

        
class Play():
    def __init__(self, user):
        self.game_over = False
        self.game_lost = False
        self.user = user
        
    def suggestion(self):
        room = self.location
        suspect = input("Who will you suggest committed the murder?")
        weapon = input("Which weapon do you suggest?")
        suggestion = Suggestion(room, suspect, weapon)
        client.send(suggestion)
        message = client.recv(1024)
        # I expect this message to be a string, saying
        # "Player x disproved your suggestion with Card" or
        # "No player could disprove your suggestion!"
        print (message)
        
    
    def accusation(self):
        USERAGREES = False
        while not USERAGREES:
            suspect = input("Whom do you accuse?")
            room = input("Where?")
            weapon = input("With what weapon?")
            print("You accuse " + suspect + " in the " + room + " with the " + weapon + ".")
            agree = input("Is this correct?")
            if agree == 'y' or agree == 'Y' or agree == 'yes' or agree == 'Yes':
                USERAGREES = True
        accusation = Accusation(room, supsect, weapon)
        client.send(accusation)
        correct = client.recv(1024)
        # I expect this message to be a boolean
        # True if the accusation is correct
        # False if the accusation is incorrect
        return correct
    
    def notebook(self):
        print (self.notebook)
        
    def play(self):
        while not self.game_over and not self.game_lost:
            action = client.rcv(1024)
            if action.type == "move":
                
                VALIDMOVE = False
                while not VALIDMOVE:
                    print("It is your turn.  Your location is " + \
                          self.user.location + ".")
                    print("Available moves are: ")
                    movelist = ''
                    for move in self.user.get_moves():
                        movelist += move + ' '
                    movelist = movelist[:-1]
                    print(movelist + '\n')
                    choice = raw_input('Where will you move?')
                    if client.valid_move(choice):
                        VALIDMOVE = True
                        self.user.location = choice
                if self.user.location.type() == 'room':
                    action = input('Would you like to (S)uggest or (A)ccuse?')
                    if action == 'S' or action == 's' \
                               or action == 'Suggest' or action == 'suggest':
                        self.suggestion()
                        update = input("Would you like to view your detective's notebook?")
                        if update == 'y' or update == 'Y' or update == 'yes' or update == 'Yes':
                            self.notebook()
                    elif action == 'A' or action == 'a' or action == 'Accuse' \
                                 or action == 'accuse':
                        result = self.accusation()
                        if result:
                            print("Your accusation was correct!  You win"!)
                            print("Game over.")
                            self.game_over = True
                        else:
                            print("Your accusation was incorrect.")
                            print("You have lost, but you can \
                                  continue to disprove suggestions.")
                            self.game_lost = True
            if action.type == "suggestion":
                print("Player " + action.player + " suggested ")
                print(action.suggestion.suspect " in the " + \
                      action.suggestion.room + " with the " + \
                      action.suggestion.weapon + ".")