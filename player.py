import chess.engine

class Player:
    COMPUTER = 1
    HUMAN = 2
    def __init__(self, name, type, engine_time_limit = 1.00):
        self.name = name
        self.type = type
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        self.engine_time_limit = engine_time_limit

    def get_move(self, board):
        if self.type == self.COMPUTER:
            result = self.engine.play(board, chess.engine.Limit(time=self.engine_time_limit))
            print("Getting move from computer player\n")
            return result.move
        else:
            move = input("Enter your move:\n")
            if (move == "auto_move" or move == ""):
                result = self.engine.play(board, chess.engine.Limit(time=1.00))
                move = result.move
            else:
                try:
                    move = chess.Move.from_uci(move)
                except:
                    return None
            return move