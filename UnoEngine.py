from timeit import default_timer as timer

from UnoPlayer import RandomPlayer, OffensivePlayer, UserPlayer
from UnoGame import UnoGame

games_to_play = 1_000

completed_moves = []
player_wins = {}

if __name__ == '__main__':
    player_types = [RandomPlayer, RandomPlayer, RandomPlayer]
    start_timer = timer()

    # creates a game with the default player count, runs it and prints results
    for i in range(games_to_play):
        game = UnoGame(player_types)
        result = game.run_game_loop()

        completed_moves.append(game.cards_played)

        try:
            player_wins[str(result)] += 1
        except KeyError:
            player_wins[str(result)] = 1

        print("SIMULATED " + str(i) + " GAMES")

    end_timer = timer()
    run_time = end_timer - start_timer

    print(str(games_to_play) + " games were played in " + str(run_time) + "s")
    print("for an average runtime of " + str(games_to_play/run_time) + " games per second")
    print(player_wins)
    print(sum(completed_moves)/len(completed_moves))


