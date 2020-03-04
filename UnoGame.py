import random
import time

class UnoGame:

    # a modifiable point goal for future use with the tally function
    point_goal = 500

    DEBUG = False

    NUMS_ENABLED = True
    REVERSE_ENABLED = True
    DRAW_ENABLED = True
    SKIP_ENABLED = True
    WILD_ENABLED = True
    WILD_DRAW_ENABLED = True

    def __init__(self, player_classes):
        # the cards that are face down and have yet to be drawn
        self.deck = []
        # the cards face up that have been played in the past
        # Note: discard[-1] is current card in pla
        self.discard = []
        # the current players playing the game
        self.players = []

        # keeps track of how many moves it took the game to play
        # a move happens when a player plays a card
        self.move_number = 1

        self.current_player = 0
        self.ordered_to_right = False

        self.setup_deck()

        # setup players
        for i in range(0, len(player_classes)):

            # create all random players for now
            player = player_classes[i](self)

            # give each player 7 cards to start off with
            for j in range(7):
                card = self.__pick_random_card()
                player.deck.append(card)

            # add the player to the game
            self.players.append(player)

        # pick first card
        self.discard.append(self.__pick_random_card())

    def run_game_loop(self):

        while True:
            print("---------------------------------")
            print("MOVE #" + str(self.move_number))
            print("Player " + str((self.current_player % len(self.players))+1) + " to move")

            card_count = len(self.discard) + len(self.deck)

            for player in self.players:
                card_count += len(player.deck)

            current_card = self.discard[-1]
            is_first_move = self.move_number == 1
            current_player_object = self.players[self.current_player % len(self.players)]

            print("THE CURRENT CARD IS: " + current_card)
            # print("PLAYED DISCARD HAS: " + str(len(self.discard)))
            # print("FREE DECK HAS: " + str(len(self.deck)))

            i = 1
            for player in self.players:
                print("Player " + str(i) + ": " + str(len(player.deck)))
                i += 1

            # OBSERVE CARD
            if current_card.startswith('o'):
                # if observe flag then play card
                # play card function will play as if card before
                self.play_card(current_player_object)
                # then remove all flags from stack so they're not being copied around
            # SKIP CARD
            elif current_card.endswith('s'):
                self.push_observe_card(current_card)
                self.goto_next_player(True)
            # wild draw 4 - DONEish
            elif current_card.endswith('wd'):
                if is_first_move:
                    self.discard.append(self.__pick_random_card())
                    continue
                else:
                    for _ in range(4):
                        self.draw_card(current_player_object)
                    self.push_observe_card(current_card)
                    self.goto_next_player()
            # draw 2 - DONE
            elif current_card.endswith('d'):
                if is_first_move:
                    # if first card is draw just skip player
                    self.goto_next_player()
                else:
                    # otherwise draw 2 cards and goto next guy
                    for _ in range(2):
                        self.draw_card(current_player_object)
                    self.push_observe_card(current_card)
                    self.goto_next_player()
            # REVERSE CARD
            elif current_card.endswith('r'):
                if is_first_move:
                    self.ordered_to_right = not self.ordered_to_right
                    self.play_card(current_player_object)
                    self.goto_next_player()
                else:
                    self.ordered_to_right = not self.ordered_to_right
                    self.push_observe_card(current_card)
                    self.goto_next_player(True)
                    continue
            # WILD CARD
            elif current_card.endswith('w'):
                color = current_player_object.pick_color()

                if is_first_move:
                    self.push_observe_card(color + current_card)
                    self.play_card(current_player_object)
                    self.goto_next_player()
                else:
                    self.play_card(current_player_object)
            else:
                self.play_card(current_player_object)

            self.move_number += 1

            #  if person has no cards left
            if len(current_player_object.deck) == 0:
                return self.current_player % len(self.players)
            print("---------------------------------")
            time.sleep(3)

    def push_observe_card(self, card):
        self.discard.append('o'+card)

    def purge_observe_flags(self):
        for card in self.deck:
            if card.startswith('o'):
                self.deck.remove(card)

    def play_card(self, player):
        card = player.play_card()

        if card is None:
            self.draw_card(player)
        elif card in player.deck:
            player.deck.remove(card)

            if card == 'w' or card == 'wd':
                card = player.pick_color() + card

            self.discard.append(card)
        else:
            print("ERROR: Player playing card they don't have")
            print(player.deck)
            print(card)
            exit(-1)

        self.goto_next_player()

    def can_play_card(self, card):
        current_card = self.discard[-1]

        if current_card.startswith('o'):
            current_card = self.discard[-2]

        return card.startswith(current_card[0]) or card.endswith(current_card[-1]) or card.startswith('w')

    def goto_next_player(self, skip=False):
        n = 2 if skip else 1
        self.current_player += n if self.ordered_to_right else -n

    def draw_card(self, player):
        card = self.__pick_random_card()
        player.deck.append(card)

    def setup_deck(self):
        colors = ['r', 'y', 'g', 'b']

        # For each color
        for i in range(4):

            if UnoGame.NUMS_ENABLED:
                # add a single zero
                self.deck.append(colors[i] + '0')

                # add two of each number 1-9
                for n in range(1, 10):
                    self.deck.append(colors[i] + str(n))
                    self.deck.append(colors[i] + str(n))

            # add two skip, draw two, and reverse cards

            if UnoGame.SKIP_ENABLED:
                 # S - skip
                self.deck.append(colors[i] + 's')
                self.deck.append(colors[i] + 's')

            if UnoGame.DRAW_ENABLED:
                # D - Draw 2
                self.deck.append(colors[i] + 'd')
                self.deck.append(colors[i] + 'd')

            if UnoGame.REVERSE_ENABLED:
                # R - Reverse
                self.deck.append(colors[i] + 'r')
                self.deck.append(colors[i] + 'r')

        # independent of color, add 4 wild and wild draw four cards

        # W - WILD
        # WD - WILD DRAW 4
        for _ in range(4):
            if UnoGame.WILD_ENABLED:
                self.deck.append('w')
            if UnoGame.WILD_DRAW_ENABLED:
                self.deck.append('wd')

    # removes card from deck and returns it
    def __pick_random_card(self):
        if len(self.deck) > 0:
            card = self.deck[random.randint(0, len(self.deck)-1)]
            self.deck.remove(card)
            return card
        else:
            #reshuffle


            print('RESHUFFLE')
            # print('------ WAS ------')
            # print(len(self.deck))
            # print(len(self.discard))
            # print('------ NOW ------')

            self.deck = self.discard[:]


            if self.deck[-1].startswith('o'):
                self.discard = [self.deck[-2], self.deck[-1]]
                self.deck.remove(self.deck[-1])
                self.deck.remove(self.deck[-2])
            else:
                self.discard = [self.deck[-1]]
                self.deck.remove(self.deck[-1])

            self.generalize_wildcards()
            self.purge_observe_flags()

            # print(len(self.deck))
            # print(len(self.discard))

            return self.__pick_random_card()

    def generalize_wildcards(self):
        for i in range(len(self.deck)-1):
            if self.deck[i].endswith('w'):
                self.deck[i] = 'w'
            if self.deck[i].endswith('wd'):
                self.deck[i] = 'wd'

    def tally_points(self):
        points = 0
        for player in self.players:
            for card in player.deck:
                if card.endswith('s') or card.endswith('r') or card.endswith('d'):
                    points += 20
                    player.deck.remove(card)
                elif card.startswith('w'):
                    points += 50
                else:
                    points += int(card[-1])

        return points
