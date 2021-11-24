import chess
import chess.engine
import player
import command_queue
import sensor_space_mapping
from led_manager import LedManager
import time

class HumanBoardPlayer(player.Player):
    def get_move(self, board, led_manager = None):
        legal_moves = board.legal_moves
        queue = command_queue.CommandQueue()
        queue.reset_queue() # TODO not sure this is a good idea
        from_square = None
        print("Waiting for move")
        while from_square is None:
            from_square = queue.dequeue()
            if from_square is None:
                continue
            (board_id, space_id, event_type) = from_square.split(":")
            if event_type == "occupied":
                # If we got an event saying that a piece has been placed, we must have missed an event or something went wrong. Reset.
                queue.reset_queue()
                from_square = None
            else:
                from_square = sensor_space_mapping.MAPPING.get(board_id + ":" + space_id, None)
            time.sleep(0.25)
        
        if led_manager is not None:
            for legal_move in legal_moves:
                if from_square == chess.square_name(legal_move.from_square):
                    led_manager.illuminate_square(chess.square_name(legal_move.from_square), (255,0,255), LedManager.LIGHTING_TYPE_INNER, False)
                    led_manager.illuminate_square(chess.square_name(legal_move.to_square), (0,0,255), LedManager.LIGHTING_TYPE_INNER, True)

        to_square = None
        while to_square is None:
            to_square = queue.dequeue()
            if to_square is None:
                continue
            (board_id, space_id, event_type) = to_square.split(":")
            if event_type == "empty":
                # If we got an event saying that a piece has been removed, we must have missed an event or something went wrong. Reset.
                queue.reset_queue()
                to_square = None
            else:
                to_square = sensor_space_mapping.MAPPING.get(board_id + ":" + space_id, None)
            time.sleep(0.25)
            
        move = from_square + to_square
        print("Got move: " + move)
        try:
            move = chess.Move.from_uci(move)
        except:
            return (None, False)
        return (move, True)
        
                
        # requires_robot_to_move = False
        # move_input = input("Enter your move in UCI format:\n")
        # if (move_input == "auto_move" or move_input == ""):
        #     result = self.engine.play(board, chess.engine.Limit(time=1.00))
        #     return (result.move, True)
        # else:
        #     try:
        #         move = chess.Move.from_uci(move_input)
        #         requires_robot_to_move = False
        #     except:
        #         return (None, False)
        # return (move, requires_robot_to_move)
