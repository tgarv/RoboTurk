import chess.engine
import player

class HumanCliPlayer(player.Player):
    def get_move(self, board, led_manager = None):
        requires_robot_to_move = True
        move_input = input("Enter your move in UCI format:\n")
        if (move_input == "auto_move" or move_input == ""):
            result = self.engine.play(board, chess.engine.Limit(time=1.00))
            return (result.move, True)
        else:
            try:
                move = chess.Move.from_uci(move_input)
                requires_robot_to_move = False
            except:
                return (None, False)
        return (move, requires_robot_to_move)
