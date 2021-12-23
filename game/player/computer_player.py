import chess.engine
from player import player


class ComputerPlayer(player.Player):
    def get_move(self, board, led_manager):
        result = self.engine.play(
            board, chess.engine.Limit(time=0.1 * self.difficulty, depth=self.difficulty)
        )
        print("Getting move from computer player\n")
        return (result.move, True)
