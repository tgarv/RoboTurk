import chess.engine
import chess

from config import config
from led_manager import LedManager
from move_wrapper import MoveWrapper


class Player:
    HUMAN = 1
    COMPUTER = 2
    HUMAN_BOARD = 3
    # In the future, we would have even more granular types: remote player (via chess.com or lichess, maybe?); human player via robotic board (current "human" player is just via CLI)

    def __init__(self, name, type, difficulty=1, engine=None):
        self.name: str = name
        self.type: int = type
        self.engine: chess.engine.SimpleEngine = (
            engine
            if engine
            else chess.engine.SimpleEngine.popen_uci(config.get_stockfish_location())
        )
        self.difficulty: int = difficulty
        self.engine.configure({"Skill Level": self.difficulty})

    def get_move(
        self, board: chess.Board, led_manager: LedManager = None
    ) -> MoveWrapper:
        """
        Get a move from the player. If the move is calculated by the engine, then the robot needs to move the piece. If the move is made by the player, then the robot does not need to move it.

        :param board: The board object for the current game
        :param led_manager: The LED Manager object for the board
        :returns: A tuple of (Move, bool), giving the move to make and whether or not the robot needs to move the piece.
        """
        raise Exception("Can't call get_move() on base Player class")

    def is_human(self) -> bool:
        return self.type == self.HUMAN

    def is_valid_type(type: str) -> bool:
        return type in [Player.HUMAN, Player.COMPUTER, Player.HUMAN_BOARD]
