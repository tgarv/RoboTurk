from typing import Tuple, Union
import chess
import chess.engine
from command_queue import CommandQueue
from move_wrapper import MoveWrapper
from player import player
import command_queue
from config import sensor_space_mapping
from led_manager import LedManager
import time
from input_thread import InputThread, bufferLock, inputBuffer


class HumanBoardPlayer(player.Player):
    def get_move(
        self, board: chess.Board, led_manager: LedManager = None
    ) -> MoveWrapper:
        # TODO how to pass an "undo" action back up to the game? :thinking:
        legal_moves: chess.LegalMoveGenerator = board.legal_moves
        queue: CommandQueue = command_queue.CommandQueue()
        queue.reset_queue()  # TODO not sure this is a good idea
        from_square: str = None
        to_square: str = None

        input_thread: InputThread = InputThread()
        input_thread.start()

        print(
            "Move a piece, enter a move, or enter the location of a piece to see all valid moves for that piece"
        )

        led_manager.initialize_checkerboard(board.piece_map())

        while from_square is None:
            led_manager.flash_piece_colors()
            time.sleep(0.1)
            command = self.get_command_from_input_thread(board)
            if isinstance(command, MoveWrapper):
                # Kind of a messy way to return an "undo" move
                return command
            else:
                from_square, to_square = command

            if from_square is None:
                from_square = self.get_square_from_command_queue(queue, "empty")
                time.sleep(0.25)

        valid_destination_squares = self.illuminate_valid_moves(
            led_manager, from_square, legal_moves
        )

        if to_square is None:
            print(
                "Place a piece or enter a destination square. Options are: "
                + ",".join(valid_destination_squares)
            )

        while to_square is None:
            time.sleep(0.1)
            command = self.get_command_from_input_thread(board)
            if isinstance(command, MoveWrapper):
                # Kind of a messy way to return an "undo" move
                return command
            else:
                square_1, square_2 = command
            if square_1 is not None:
                to_square = square_1
            else:
                to_square = self.get_square_from_command_queue(queue, "occupied")

        move = from_square + to_square
        print("Got move: " + move)
        try:
            move = chess.Move.from_uci(move)
        except:
            return MoveWrapper(None, MoveWrapper.TYPE_NONE)
        return MoveWrapper(move)

    def get_command_from_input_thread(
        self, board: chess.Board
    ) -> Union[Tuple[str, str], MoveWrapper]:
        terminal_input: str = None
        square_1: str = None
        square_2: str = None

        bufferLock.acquire()
        if len(inputBuffer) > 0:
            terminal_input = inputBuffer.pop()
            terminal_input = terminal_input.rstrip("\n")
        bufferLock.release()

        if terminal_input is not None:
            if terminal_input == "" or terminal_input == "auto_move":
                result = self.engine.play(board, chess.engine.Limit(time=1.00))
                move = str(result.move)
                square_1 = move[:2]
                square_2 = move[2:]
            if terminal_input == "undo":
                return MoveWrapper(None, MoveWrapper.TYPE_UNDO)
            elif len(terminal_input) == 2:
                square_1 = terminal_input
                square_2 = None
            elif len(terminal_input) == 4:
                square_1 = terminal_input[:2]
                square_2 = terminal_input[2:]
        return square_1, square_2

    def get_square_from_command_queue(self, queue: CommandQueue, expected_event: str):
        event = queue.dequeue()
        if event is None:
            return None
        try:
            (board_id, space_id, event_type) = event.split(":")
        except ValueError:
            # Event doesn't have enough parts
            return None
        if event_type != expected_event:
            # If we got the wrong type of event, we must have missed an event or something went wrong. Reset.
            queue.reset_queue()
            return None
        else:
            return sensor_space_mapping.MAPPING.get(board_id + ":" + space_id, None)

    def illuminate_valid_moves(
        self,
        led_manager: LedManager,
        from_square: str,
        legal_moves: chess.LegalMoveGenerator,
    ):
        valid_destination_squares = []
        if led_manager is not None:
            for legal_move in legal_moves:
                if from_square == chess.square_name(legal_move.from_square):
                    valid_destination_squares.append(
                        chess.square_name(legal_move.to_square)
                    )
                    led_manager.illuminate_square(
                        chess.square_name(legal_move.to_square),
                        (0, 0, 255),
                        LedManager.LIGHTING_TYPE_INNER,
                        False,
                    )
            if len(valid_destination_squares) > 0:
                led_manager.illuminate_square(
                    from_square,
                    (255, 0, 255),
                    LedManager.LIGHTING_TYPE_INNER,
                    True,
                )
        return valid_destination_squares
