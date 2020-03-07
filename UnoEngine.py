from timeit import default_timer as timer
import concurrent.futures

from UnoPlayer import RandomPlayer, OffensivePlayer, UserPlayer
from UnoGame import UnoGame

games_to_play = 1 0_000

completed_moves = []
player_wins = {}


# runs a game and returns who won and the number of cards played in a tuple
def run_game():
    game = UnoGame(player_types)
    result = game.run_game_loop()

    return result, game.cards_played


if __name__ == '__main__':
    player_types = [RandomPlayer, RandomPlayer, RandomPlayer]
    start_timer = timer()

    # Runs the games in parallel and writes the result upon completion
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(run_game) for _ in range(games_to_play)]

        for game_result in concurrent.futures.as_completed(results):
            p_result = game_result.result()[0]

            completed_moves.append(game_result.result()[1])

            try:
                player_wins[str(p_result)] += 1
            except KeyError:
                player_wins[str(p_result)] = 1

            print(f"{sum(player_wins.values())}/{games_to_play}")

    end_timer = timer()
    run_time = end_timer - start_timer

    print(f"{str(games_to_play)} games were played in {str(run_time)}s")
    print(f"for an average runtime of {str(games_to_play/run_time)} games per second")
    print(player_wins)
    print(sum(completed_moves)/len(completed_moves))


