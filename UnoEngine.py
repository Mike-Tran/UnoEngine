import random
from timeit import default_timer as timer
import concurrent.futures

from UnoPointSeries import UnoPointSeries
from UnoPlayer import RandomPlayer, OffensivePlayer, UserPlayer


# This program simulates games of the card game Uno
# The statistical superiority of various strategies can be tested by subclassing UnoPlayer
# My long term goal is to learn and apply machine learning and game theory techniques and eventually possibly build
# a Uno Engine similar to a 'chess engine' (if possible in such a non-deterministic game)

games_to_play = 10_000

# This should usually be True unless you have some magical reason I couldn't think of why it shouldn't be
# When a UserPlayer is in the game it automatically defaults to False so user input can be handled reasonably
parallel = True

completed_hands = []
completed_moves = []
player_wins = {}


# runs a game and returns who won and the number of cards played in a tuple
def run_game():
    game = UnoPointSeries(player_types)
    result = game.run()

    return result


if __name__ == '__main__':
    # Note there must be at least 3+ players because custom 2 player rules haven't been added yet
    player_types = [RandomPlayer, RandomPlayer, RandomPlayer, RandomPlayer]
    start_timer = timer()

    # If receiving user input do not run concurrently
    if UserPlayer in player_types:
        parallel = False

    if parallel:
        # Runs the games in parallel and writes the result upon completion
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(run_game) for _ in range(games_to_play)]

            for game_result in concurrent.futures.as_completed(results):
                p_result = game_result.result()[0]

                try:
                    player_wins[str(p_result)] += 1
                except KeyError:
                    player_wins[str(p_result)] = 1

                completed_hands.append(game_result.result()[1])
                completed_moves.append(game_result.result()[2])

                print(f"{sum(player_wins.values())}/{games_to_play}")
    else:
        for i in range(games_to_play):
            game_result = run_game()

            try:
                player_wins[game_result[0]] += 1
            except KeyError:
                player_wins[game_result[0]] = 1

            completed_hands.append(game_result[1])
            completed_moves.append(game_result[2])

            print(f"{i}/{games_to_play}")

    end_timer = timer()
    run_time = end_timer - start_timer

    hands_per_game = sum(completed_hands) / len(completed_hands)
    moves_per_game = sum(completed_moves) / len(completed_moves)
    moves_per_hand = moves_per_game / hands_per_game

    print(f"{games_to_play:,} games were played in {run_time:.2f}s")
    print(f"for an average runtime of {games_to_play/run_time:,.2f} games per second")
    print(f"or {moves_per_game*games_to_play/run_time:,.2f} moves per second")
    print(player_wins)


    print("Avg hands/game: " + str(hands_per_game))
    print("Avg moves/game: " + str(moves_per_game))
    print("Avg moves/hand: " + str(moves_per_hand))




