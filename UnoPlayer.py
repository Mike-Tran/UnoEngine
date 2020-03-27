import random
import operator
import scipy.stats

# Subclass this in order to make custom strategies
class UnoPlayer:

    def __init__(self, game):
        # the game the player is currently in
        self.game = game
        # the cards the player has in their hand is deck
        self.deck = []

    # not implemented - left up to subclasses
    def play_card(self):
        print("ERROR: Undefined card play function")
        exit(-1)

    # returns the cards the player is allowed to play based on the game rules
    def valid_cards(self):
        return list(filter(self.game.can_play_card, self.deck))

    # checks if a card is of a certain color
    def card_is_color(self, card, color):
        return card.startswith(color)

    # not implemented - left up to subclasses
    def pick_color(self):
        print("ERROR: Undefined color picking behavior for player")
        exit(-1)

# Picks cards and colors at random
class RandomPlayer(UnoPlayer):
    # chooses a random valid card and returns it to play
    def play_card(self):
        valid_cards = self.valid_cards()

        if len(valid_cards) == 0:
            return None
        else:
            return valid_cards[random.randint(0, len(valid_cards)-1)]

    def pick_color(self):
        return ['r', 'g', 'b', 'y'][random.randint(0, 3)]

# Uses this strategy found on wikipedia
# “An offensive strategy would be holding on to Wild and Wild Draw Four cards because they can be played near the end
# of the hand in order to go out (when it's harder to play a matching card).
# However, an offensive strategy would suggest playing a 0 when the player wants to continue on the current color, because it is
# less likely to be matched by another 0 of a different color (there is only one 0 of each color, but two of each 1–9).
class OffensivePlayer(UnoPlayer):

    # Hold Wild and Wild Draw until end
    # Play 0 if want to continue current color
    def play_card(self):
        valid_cards = self.valid_cards()
        cards_except_wild = list(filter(self.__exclude_wild, valid_cards))

        if len(valid_cards) == 0:
            return None

        # if have valid cards other than wild cards
        if len(cards_except_wild) > 0:
            # if I have a zero card I can play
            if len(list(filter(self.is_zero, cards_except_wild))) > 0:

                # see what color I have the most of
                amount_per_color = {
                    'r': self.number_of_cards_for_color('r', valid_cards),
                    'g': self.number_of_cards_for_color('g', valid_cards),
                    'b': self.number_of_cards_for_color('b', valid_cards),
                    'y': self.number_of_cards_for_color('y', valid_cards)
                }

                # play zero of color I have the most of
                max_sorted_colors = max(amount_per_color.items(), key=operator.itemgetter(1))

                for color in max_sorted_colors:
                    if color + '0' in valid_cards:
                        return color + '0'

            else:
                # if I have no zeros just play a random non-wild card
                return cards_except_wild[random.randint(0, len(cards_except_wild)-1)]
        else:
            # else play valid card which is gonna be a wild
            return valid_cards[random.randint(0, len(valid_cards)-1)]

    def __exclude_wild(self, card):
        return 'w' in card

    # TODO: Generize and move?
    def is_zero(self, card):
        return card.endswith('0')

    def number_of_cards_for_color(self, color, cards):
        return len(list(filter(lambda card: self.card_is_color(card, color), cards)))

    def pick_color(self):
        amount_per_color = {
            'r': self.number_of_cards_for_color('r', self.deck),
            'g': self.number_of_cards_for_color('g', self.deck),
            'b': self.number_of_cards_for_color('b', self.deck),
            'y': self.number_of_cards_for_color('y', self.deck)
        }

        max_sorted_colors = max(amount_per_color.items(), key=operator.itemgetter(1))
        return max_sorted_colors[0]

# A player that recieves user input - used for debugging
class UserPlayer(UnoPlayer):
    def pick_color(self):

        color = ''

        while True:
            color = input("Please pick a color. [R, Y, G, B]: ")
            if color.lower() in ['r', 'g', 'b', 'y']:
                break

        return color

    def play_card(self):

        print("Your cards are " + str(self.deck) + " and there are (" + str(len(self.deck)) + ") ")

        if len(self.valid_cards()) == 0:
            print("Drawing... ")
            return None

        card = ''
        while True:
            card = input("Please play a card. " + str(self.valid_cards()) + ": ")
            if card in self.valid_cards():
                break
        return card

# TODO: This is a work in progress and unfinished

# Remembers what cards have been played and decides to play the card with the lowest probability of continuation
# If multiple continuations are equally probable it chooses based on what they are most likely to be able to conintue)

# NOTE: This currently doesn't take into account non-standard game options, ex if certain card types are disabled
class KeenPlayer(UnoPlayer):

    def play_card(self):
        pass


    # These 3 functions give the percentage of the given card types the player has
    # TODO: Refactor into one function

    def __percentage_same_number(self, number):

        condition = lambda item: item.endswith(number)

        amount_seen = sum(list(filter(condition, self.__cards_without_observe(self.game.discard))))
        amount_have = sum(list(filter(condition, self.deck)))
        amount_total = 4 if number.endswith('0') else 8

        return (amount_total - amount_have - amount_seen) / amount_total

    def __percentage_same_color(self, color):

        condition = lambda item: item.startswith(color)

        amount_seen = sum(list(filter(condition, self.__cards_without_observe(self.game.discard))))
        amount_have = sum(list(filter(condition, self.deck)))
        amount_total = 25

        return (amount_total - amount_have - amount_seen) / amount_total

    def __percentage_wild(self):

        condition = lambda item: item.contains('w')

        amount_seen = sum(list(filter(condition, self.__cards_without_observe(self.game.discard))))
        amount_have = sum(list(filter(condition, self.deck)))
        amount_total = 8

        return (amount_total - amount_have - amount_seen) / amount_total

    #TODO: In future just generalize function in UnoGame
    def __cards_without_observe(self, cards):
        return list(filter(lambda item: not item.startswith('o'), self.game.discard))

# TODO
# If next person has less cards it will play a special card or change the color if it can
class ScaredPlayer(UnoPlayer):

    def play_card(self):
        pass

    def pick_color(self):
        pass

    def next_has_less_cards(self):
        return False