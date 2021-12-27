import chess
import chess.engine
from led_manager import LedManager
from move_wrapper import MoveWrapper
from player import player


class ComputerPlayer(player.Player):
    def get_move(self, board: chess.Board, led_manager: LedManager) -> MoveWrapper:
        result = self.engine.play(
            board, chess.engine.Limit(time=0.1 * self.difficulty, depth=self.difficulty)
        )
        print("Getting move from computer player\n")
        return MoveWrapper(result.move)
