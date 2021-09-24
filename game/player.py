import chess.engine

class Player:
    # @TODO use Player as base class, add subclasses for types
    HUMAN = 1
    COMPUTER = 2

    def __init__(self, name, type, engine_time_limit = 1.00):
        self.name = name
        self.type = type
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        self.engine_time_limit = engine_time_limit

    def get_move(self, board):
        # Get a move from the player. If the move is calculated by the engine, then the robot needs to move the piece. If the move is made by the player, then the robot does not need to move it.
        # Returns a tuple of (Move, bool), giving the move to make and whether or not the robot needs to move the piece.
        requires_robot_to_move = True
        if self.type == self.COMPUTER:
            result = self.engine.play(board, chess.engine.Limit(time=self.engine_time_limit))
            print("Getting move from computer player\n")
            return (result.move, requires_robot_to_move)
        else:
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

    def is_human(self):
        return self.type == self.HUMAN

    def is_valid_type(self, type):
        return type in [self.HUMAN, self.COMPUTER]