import chess
import chess.engine
from move_wrapper import MoveWrapper
from player.player import Player
import head
import game_configurator
import led_manager
import board_monitor
from config import config

import threading


class Game:
    def __init__(self, player_white, player_black, board=None, engine=None):
        self.player_white = player_white
        self.player_black = player_black
        self.board = board if board else chess.Board()
        self.engine = (
            engine
            if engine
            else chess.engine.SimpleEngine.popen_uci(config.get_stockfish_location())
        )
        self.led_manager = led_manager.LedManager.getInstance()
        self.led_manager.initialize_checkerboard(self.board.piece_map())

        # Head isn't really used, but the code was written when this was planned to be a robotic board
        self.head = head.Head()

        # Start a thread with the board monitor
        threading.Thread(
            target=lambda: board_monitor.run()
        ).start()

    def play(self):
        """The main game loop - play through each turn until a winner is determined"""
        while True:
            # TODO improve game end logic with self.board.outcome(). This has statuses for all the various win/draw conditions.
            player = self.get_current_player()
            if self.board.can_claim_draw():
                print(player.name + " claims draw")
                break
            else:
                self.do_turn()
                if self.board.is_game_over():
                    print(player.name + " wins!")
                    break

        print("Game over")

    def do_turn(self):
        """Handle a single turn for the current player"""
        player: Player = self.get_current_player()
        move_complete: bool = False
        while not move_complete:
            info = self.engine.analyse(self.board, chess.engine.Limit(time=0.5))
            print(info["score"])
            print(self.board)
            print(player.name + "'s turn")

            move_wrapper: MoveWrapper = player.get_move(self.board, self.led_manager)
            move = move_wrapper.move

            if move_wrapper.type == MoveWrapper.TYPE_UNDO:
                try:
                    move = self.board.pop()
                except IndexError:
                    continue
                move_complete = True
                # TODO should undo twice if you're playing a computer player, but then we need to figure out how to highlight that on the board
            elif not move or not (move in self.board.legal_moves):
                print("Illegal move - try again")
                continue
            else:
                is_capture = self.board.is_capture(move)
                self.board.push(move)
                move_complete = True

            if move_complete:
                self.led_manager.initialize_checkerboard(self.board.piece_map())
                self.led_manager.illuminate_square(chess.square_name(move.from_square))
                # TODO use is_capture to highlight captured piece
                self.led_manager.illuminate_square(
                    chess.square_name(move.to_square), (255, 0, 0)
                )

    def get_current_player(self):
        """
        Get the Player object for the current turn

        :returns: Player
        """
        if self.board.turn == chess.WHITE:
            return self.player_white
        return self.player_black

    def get_coordinates_for_square(self, square):
        """
        Get a tuple of (row, column) coordinates for the given square number

        :param square: The square number (in the range (1, 64))
        :returns: tuple of (row, column) integers
        """
        # square is in the range (1, 64), so we need to translate that to row/column
        column = square % 8
        row = square // 8
        return (column, row)

    def move_piece(self, move, is_capture):
        """
        Physically move the piece from and to the cells defined in the provided move object
        NB: This is not actually implemented in hardware, so it's just for a theoretical future board that includes robotic movements
        :param move: Move
        :param is_capture: Whether or not the move captured a piece
        """
        # TODO implement this for captures:
        # Get piece type at move.to_square
        # Get the off-grid location for that piece (where it's stored when it has been captured)
        # Move the head to the captured piece's location
        # Move the captured piece from its location to its storage location
        # Move the head back to the capturing piece's location
        # Move the capturing piece to move.to_square
        if is_capture:
            piece = self.board.piece_at(move.to_square)
            print(
                "Captured piece with type %s"
                % (piece.piece_type if piece is not None else chess.PAWN)
            )

        # TODO also need to implement promotions
        # This is tricky - do we need an extra of every piece type? (e.g. if you promote to Queen but your Queen still exists, where do we get the extra Queen from?)
        # Technically, you could need multiple of every piece type, but that's annoying to deal with.
        # Assuming we have an extra of every type, the logic would be:
        # Move the pawn (that's being promoted) to its off-grid location
        # Get the promotion piece type
        # Get the (off-grid) location for the extra piece of that type
        # Move the head to that location
        # Move the piece from that location to the promotion square

        from_column, from_row = self.get_coordinates_for_square(move.from_square)
        to_column, to_row = self.get_coordinates_for_square(move.to_square)
        print(
            "Moving piece from "
            + str((from_column, from_row))
            + " to "
            + str((to_column, to_row))
        )
        # Turn off the magnet (probably unnecessary, but just in case)
        self.head.set_magnet(False)
        # Move the head under the piece to move
        self.head.move_to_position(from_column, from_row)
        # Turn on the magnet to "grab" the piece
        self.head.set_magnet(True)
        # Move the head (and the piece) to the destination
        self.head.move_to_position(to_column, to_row)
        # Turn off the magnet to "drop" the piece
        self.head.set_magnet(False)


if __name__ == "__main__":
    configurator = game_configurator.GameConfigurator()
    while True:
        print("Starting a new game!")
        game = configurator.get_game()
        game.play()
