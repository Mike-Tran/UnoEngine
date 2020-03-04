import sys

from UnoPlayer import RandomPlayer, OffensivePlayer, UserPlayer
from UnoGame import UnoGame

default_player_count = 4

# for future use to allow command line choosing of player count
arguments = ['pc']
argument_values = {}

# keeps track of each players points and the number of games played
point_count = {}

games_to_play = 1_000

completed_moves = []
player_wins = {}


# for future use of command line arguments
def load_args():
    argument_count = len(sys.argv) - 1
    position = 0

    in_value = False

    while argument_count >= position:
        arg = sys.argv[position].replace('-', '')

        if not in_value:
            if arg in arguments:
                in_value = True
        else:
            last_stripped = sys.argv[position - 1].replace('-', '')
            argument_values[last_stripped] = arg
            in_value = False

        position += 1


if __name__ == '__main__':
    # load_args()
    # start game based on loaded args 
    #print(argument_values)

    # sys.setrecursionlimit(10)

    # creates a game with the default player count, runs it and prints results
    for i in range(0, games_to_play):
        player_types = [OffensivePlayer, UserPlayer, RandomPlayer]
        game = UnoGame(player_types)
        result = game.run_game_loop()

        completed_moves.append(game.move_number)

        try:
            player_wins[str(result)] += 1
        except KeyError:
            player_wins[str(result)] = 1

    print(str(games_to_play) + " were played")
    print(player_wins)
    print(sum(completed_moves)/len(completed_moves))


