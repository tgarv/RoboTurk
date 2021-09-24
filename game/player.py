import chess.engine

class Player:
    HUMAN = 1
    COMPUTER = 2

    def __init__(self, name, type, engine_time_limit = 1.00):
        self.name = name
        self.type = type
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        self.engine_time_limit = engine_time_limit

    def get_move(self, board):
        raise Exception("Can't call get_move() on base Player class")

    def is_human(self):
        return self.type == self.HUMAN

    def is_valid_type(type):
        return type in [Player.HUMAN, Player.COMPUTER]