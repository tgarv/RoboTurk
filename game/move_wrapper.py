import chess


class MoveWrapper:
    TYPE_STANDARD = 1
    TYPE_UNDO = 2
    TYPE_NONE = 3

    def __init__(self, move: chess.Move, type: int = TYPE_STANDARD):
        self.move = move
        self.type = type
