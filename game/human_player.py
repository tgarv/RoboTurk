import chess.engine
import player

class HumanPlayer(player.Player):
    def get_move(self, board):
        # Get a move from the player. If the move is calculated by the engine, then the robot needs to move the piece. If the move is made by the player, then the robot does not need to move it.
        # Returns a tuple of (Move, bool), giving the move to make and whether or not the robot needs to move the piece.
        requires_robot_to_move = True
        move = input("Enter your move:\n")
        if (move == "auto_move" or move == ""):
            result = self.engine.play(board, chess.engine.Limit(time=1.00))
            move = result.move
        else:
            try:
                move = chess.Move.from_uci(move)
                requires_robot_to_move = False
            except:
                return (None, False)
        return (move, requires_robot_to_move)
