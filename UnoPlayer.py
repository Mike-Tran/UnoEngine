import random
import operator

# Players are supposed to subclass this in order to make custom strategies
class UnoPlayer:
    # the cards the player has in their hand is deck

    # the game the player is currently in

    def __init__(self, game):
        self.game = game
        self.deck = []
        pass

    def play_card(self):
        pass

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