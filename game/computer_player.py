import chess.engine
import player

class ComputerPlayer(player.Player):
    def get_move(self, board, led_manager):
        result = self.engine.play(board, chess.engine.Limit(time=self.engine_time_limit))
        print("Getting move from computer player\n")
        return (result.move, True)
