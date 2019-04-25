import chess.engine

class Player:
    COMPUTER = 1
    HUMAN = 2
    def __init__(self, name, type):
        self.name = name
        self.type = type
        if type == self.COMPUTER:
            self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
            self.engine_time_limit = 1.00

    def get_move(self, board):
        if self.type == self.COMPUTER:
            result = self.engine.play(board, chess.engine.Limit(time=self.engine_time_limit))
            print("Getting move from computer player\n")
            return result.move.uci()
        else:
            move = input("Enter your move:\n")
            return move