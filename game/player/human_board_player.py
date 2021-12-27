import chess
import chess.engine
from player import player
import command_queue
from config import sensor_space_mapping
from led_manager import LedManager
import time
from input_thread import InputThread, bufferLock, inputBuffer


class HumanBoardPlayer(player.Player):
    def get_move(self, board, led_manager=None):
        # TODO how to pass an "undo" action back up to the game? :thinking:
        legal_moves = board.legal_moves
        queue = command_queue.CommandQueue()
        queue.reset_queue()  # TODO not sure this is a good idea
        from_square = None
        to_square = None

        input_thread = InputThread()
        input_thread.start()

        print(
            "Move a piece, enter a move, or enter a square to move a piece from to see all valid moves for that piece"
        )

        while from_square is None:
            time.sleep(0.1)
            from_square, to_square = self.get_command_from_input_thread(board)

            if from_square is None:
                event = queue.dequeue()
                if event is None:
                    continue
                (board_id, space_id, event_type) = from_square.split(":")
                if event_type == "occupied":
                    # If we got an event saying that a piece has been placed, we must have missed an event or something went wrong. Reset.
                    queue.reset_queue()
                    from_square = None
                    # TODO continue here?
                else:
                    from_square = sensor_space_mapping.MAPPING.get(
                        board_id + ":" + space_id, None
                    )
                time.sleep(0.25)

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
                    chess.square_name(from_square),
                    (255, 0, 255),
                    LedManager.LIGHTING_TYPE_INNER,
                    True,
                )

        if to_square is None:
            print(
                "Place a piece or enter a destination square. Options are: "
                + ",".join(valid_destination_squares)
            )

        while to_square is None:
            time.sleep(0.1)
            square_1, square_2 = self.get_command_from_input_thread(board)
            if square_1 is not None:
                to_square = square_1
            else:
                to_square = queue.dequeue()
                if to_square is None:
                    continue
                (board_id, space_id, event_type) = to_square.split(":")
                if event_type == "empty":
                    # If we got an event saying that a piece has been removed, we must have missed an event or something went wrong. Reset.
                    queue.reset_queue()
                    to_square = None
                else:
                    to_square = sensor_space_mapping.MAPPING.get(
                        board_id + ":" + space_id, None
                    )

        move = from_square + to_square
        print("Got move: " + move)
        try:
            move = chess.Move.from_uci(move)
        except:
            return (None, False)
        return (move, True)

    def get_command_from_input_thread(self, board):
        terminal_input = None
        bufferLock.acquire()
        if len(inputBuffer) > 0:
            terminal_input = inputBuffer.pop()
            terminal_input = terminal_input.rstrip("\n")
        bufferLock.release()

        square_1 = None
        square_2 = None
        if terminal_input is not None:
            if terminal_input == "" or terminal_input == "auto_move":
                result = self.engine.play(board, chess.engine.Limit(time=1.00))
                move = str(result.move)
                square_1 = move[:2]
                square_2 = move[2:]
            elif len(terminal_input) == 2:
                square_1 = terminal_input
                square_2 = None
            elif len(terminal_input) == 4:
                square_1 = terminal_input[:2]
                square_2 = terminal_input[2:]
        return square_1, square_2
