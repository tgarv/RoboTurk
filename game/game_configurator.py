import player
import human_player
import computer_player
import game

class GameConfigurator():
    def __init__(self):
        pass

    def get_game(self):
        player1 = self.get_player("White")
        player2 = self.get_player("Black")

        return game.Game(player1, player2)

    def get_player(self, color):
        player_type = None
        while not player_type:
            try:
                player_type = int(input("Select player type for %s: 1) Human 2) Computer \n" % (color)))
                if not player.Player.is_valid_type(player_type):
                    raise Exception
            except Exception:
                player_type = None
                print("Invalid player type - try again")
            
        if player_type == player.Player.COMPUTER:
            difficulty = float(input("Select difficulty for %s player (1-10) \n" % (color)))
            return computer_player.ComputerPlayer(color, player_type, engine_time_limit=0.2 * difficulty)
        
        return human_player.HumanPlayer(color, player_type)
