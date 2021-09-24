import chess.engine

class Player:
    HUMAN = 1
    COMPUTER = 2
    # In the future, we would have even more granular types: remote player (via chess.com or lichess, maybe?); human player via robotic board (current "human" player is just via CLI)

    def __init__(self, name, type, engine_time_limit = 1.00, engine = None):
        self.name = name
        self.type = type
        self.engine = engine if engine else chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        self.engine_time_limit = engine_time_limit

    def get_move(self, board):
        """
        Get a move from the player. If the move is calculated by the engine, then the robot needs to move the piece. If the move is made by the player, then the robot does not need to move it.

        :param board: The board object for the current game
        :returns: A tuple of (Move, bool), giving the move to make and whether or not the robot needs to move the piece.
        """
        raise Exception("Can't call get_move() on base Player class")

    def is_human(self):
        return self.type == self.HUMAN

    def is_valid_type(type):
        return type in [Player.HUMAN, Player.COMPUTER]