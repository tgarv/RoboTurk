import chess
import chess.engine
from led_manager import LedManager
from move_wrapper import MoveWrapper
from player import player


class HumanCliPlayer(player.Player):
    def get_move(self, board: chess.Board, led_manager: LedManager = None):
        move_input = input("Enter your move in UCI format:\n")
        if move_input == "auto_move" or move_input == "":
            result = self.engine.play(board, chess.engine.Limit(time=1.00))
            return (result.move, True)
        else:
            try:
                move = chess.Move.from_uci(move_input)
            except:
                return MoveWrapper(None, MoveWrapper.TYPE_NONE)
        return MoveWrapper(move)
