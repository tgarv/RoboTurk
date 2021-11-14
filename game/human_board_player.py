import chess
import chess.engine
import player
import command_queue
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
            time.sleep(0.05)
        
        if led_manager is not None:
            for legal_move in legal_moves:
                if from_square == chess.square_name(legal_move.from_square):
                    led_manager.illuminate_square(chess.square_name(legal_move.from_square), (255,0,255))
                    led_manager.illuminate_square(chess.square_name(legal_move.to_square), (0,0,255))

        to_square = None
        while to_square is None:
            to_square = queue.dequeue()
            time.sleep(0.05)
            
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
