from UnoGame import UnoGame


# Point series is a number of games played until a point value is hit and someone wins
class UnoPointSeries:

    # a modifiable point goal
    point_goal = 500

    def __init__(self, players):
        self.players = players
        self.points = []
        # kept track of for data collection purposes
        self.games_played = 0
        self.moves_played = 0

        for _ in range(len(players)):
            self.points.append(0)

    # recursively plays games until a winner is reached and returned
    def run(self):
        game_over = max(self.points) >= UnoPointSeries.point_goal

        if game_over:
            return self.points.index(max(self.points)), self.games_played, self.moves_played
        else:
            game = UnoGame(self.players)
            winner_index = game.run_game_loop()
            self.points[winner_index] += game.tally_points()

            self.games_played += 1
            self.moves_played += game.cards_played

            return self.run()

