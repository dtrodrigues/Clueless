#!/usr/bin/env python
from logic import game

import logic.message as m
import pickle

class ServerError(IOError): pass
class Ignore(ServerError): pass

class Server():

    def __init__(self):
        self.game = game.Game()
        self.current_suggestion = ()
        self.game_on = False

    def invoke(self,message):

        inbound = pickle.loads(message)

        if self.game.game_over:
            raise Ignore("Game is over. No more possible moves.")
        if inbound.direction == m.FROM_SERVER:
            raise Ignore("Wrong direction for message")



        # this indicates game is ready to begin, cards should be dealt
        if inbound.typ == m.START_GAME:

            if self.game.ready_to_start == False:
                raise Ignore("Game cannot be started yet. Not enough players.")
            if self.game_on:
                raise Ignore("Game has already begun. Cannot start again.")

            self.game_on = True

            # deal the rest of the cards
            info = {}
            self.game.distribute_remaining_cards()
            for x in self.game.playerlist:
                info[x.suspect] = x.cards
            info['players']  = [x.suspect for x in self.game.playerlist]

            info['board'] = self.game.pickle_board()

            outbound = m.Message(
                direction = m.FROM_SERVER,
                typ       = m.START,
                info      = info,
                new_turn  = self.game.current_player,
                comment   = "Game is beginning. Dealing cards to players."
            )



        # add a player
        elif inbound.typ == m.ADD_ME:

            if self.game_on:
                raise Ignore("Game has already started. Cannot add players.")

            try:
                name    = inbound.info['name']
                suspect = inbound.info['suspect']

                newplayer = game.Player(name,suspect)
                self.game.add_player(newplayer)

            except game.PlayerError, errmsg:
                raise Ignore(errmsg)

            info = {}
            info['name']      = name
            info['suspect']   = suspect
            info['remaining'] = self.game.available_suspects

            outbound = m.Message(
                direction   = m.FROM_SERVER,
                typ         = m.ADD_PLAYER,
                info        = info,
                comment     = "Player has been added."
            )



        # player makes a move
        elif inbound.typ == m.MAKE_MOVE:

            suspect = inbound.info['suspect']
            coord   = inbound.info['coord']

            #if suspect != self.game.current_player:
            #    raise Ignore("It is not this player's turn.")

            success = self.game.update_player_position(suspect,coord)
            newboard = self.game.pickle_board()

            info = {}
            info['suspect'] = suspect
            info['board']   = newboard
            info['success'] = success

            outbound = m.Message(
                direction   = m.FROM_SERVER,
                typ         = m.MADE_MOVE,
                info        = info,
                comment     = "Player made move."
            )



        # player makes a suggestion
        elif inbound.typ == m.MAKE_SUGGESTION:

            suspect = inbound.info['suspect']
            if suspect != self.game.current_player:
                raise Ignore("It is not this player's turn.")
            if suspect in self.game.losers:
                raise Ignore("This player has lost and cannot suggest.")

            # suggestion should be tuple of the form (room, suspect, weapon)
            suggestion = inbound.info['suggestion']

            # send the name of the player to disprove
            # this also updates the state of the board
            disprover, cards, whoCantDisprove = self.game.check_suggestion(suggestion)

            info = {}

            info['suspect']      = suspect
            info['suggestion']   = suggestion
            info['disprover'] = disprover
            info['cards'] = cards
            info['whoCantDisprove'] = whoCantDisprove
            info['board']        = self.game.pickle_board()

            # no one can disprove
            if not disprover:

                # then it's someone elses turn now
                #new_suspect = self.game.next_turn()

                outbound = m.Message(
                    direction   = m.FROM_SERVER,
                    typ         = m.MADE_SUGGESTION,
                    info        = info,
                    #new_turn    = new_suspect, accusation can be made after a suggestion
                    comment     = "Suggestion was made and can't be disproved."
                )

            # otherwise, here's the name of the disproving suspect
            else:

                outbound = m.Message(
                    direction   = m.FROM_SERVER,
                    typ         = m.MADE_SUGGESTION,
                    info        = info,
                    comment     = "Suggestion was made and can be disproved."
                )



        # player makes an accusation
        elif inbound.typ == m.MAKE_ACCUSATION:

            suspect = inbound.info['suspect']
            if suspect != self.game.current_player:
                raise Ignore("It is not this player's turn.")
            if suspect in self.game.losers:
                raise Ignore("This player has lost already and cannot accuse.")

            # accusation should be tuple of the form (room, suspect, weapon) 
            accusation = inbound.info['accusation']

            success = self.game.check_accusation(accusation)
            newboard = self.game.pickle_board()

            info = {}
            info['suspect'] = suspect
            info['accusation'] = accusation
            info['board'] = newboard

            if success:
                self.game.end_game()

                info['gameover'] = True

                outbound = m.Message(
                    direction   = m.FROM_SERVER,
                    typ         = m.WON_GAME,
                    info        = info,
                    comment     = "Suspect has won. Game is over."
                )

            else:
                self.game.declare_loser(suspect)

                info['gameover'] = False
                # maybe invoke next turn here and return the name of the next
                # suspect
                new_suspect = self.game.next_turn()

                # this means there are no more suspects and the game is over
                if suspect == new_suspect:
                    info['gameover'] = True
                    new_suspect = ""

                outbound = m.Message(
                    direction   = m.FROM_SERVER,
                    typ         = m.LOST_GAME,
                    info        = info,
                    new_turn    = new_suspect,
                    comment     = "Suspect made bad accusation and loses."
                )



        # disproval
        elif inbound.typ == m.DISPROVE: 

            shower = inbound.info['shower']
            card    = inbound.info['card']
            showTo = inbound.info['showTo']

            # next turn here
            new_suspect = self.game.next_turn()

            info = {}
            info['shower'] = shower
            info['card']   = card
            info['showTo'] = showTo

            outbound = m.Message(
                direction   = m.FROM_SERVER,
                typ         = m.WAS_DISPROVED,
                info        = info,
                new_turn    = new_suspect,
                comment     = "Suggestion was disproved by suspect using card."
            )

        # player ends their turn
        elif inbound.typ == m.END_TURN:

            new_suspect = self.game.next_turn()

            outbound = m.Message(direction = m.FROM_SERVER,
                    typ = m.TURN_ENDED, new_turn = new_suspect)


        # erroneous input
        else:
            raise ServerError("Unknown inbound message type.")


        # this will provide the list of available moves for the next player
        if outbound.new_turn:
            outbound.info['moves'] = self.game.board.available_moves(outbound.new_turn)


        # last step for everybody
        outbound = pickle.dumps(outbound)
        return outbound
