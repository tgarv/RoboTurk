import player
import game

class GameConfigurator():
    def __init__(self):
        pass

    def get_game(self):
        player1 = self.get_player("White")
        player2 = self.get_player("Black")

        return game.Game(player1, player2)

    def get_player(self, color):
        # @TODO validation
        player_type = int(input("Select player type for %s: 1) Human 2) Computer" % (color)))
        if player_type == player.Player.COMPUTER:
            difficulty = float(input("Select difficulty for %s player (1-10)" % (color)))
            return player.Player(color, player_type, engine_time_limit=0.1 * difficulty)
        return player.Player(color, player_type)
