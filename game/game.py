import chess
import chess.engine
import head
import game_configurator
import command_queue
import led_manager
import server

import threading

class Game:
    # @TODO clean this up
    STOCKFISH_LOCATION_RPI = "/usr/games/stockfish"
    STOCKFISH_LOCATION_MACOS = "/usr/local/bin/stockfish"

    def __init__(self, player_white, player_black, board = None, engine = None):
        self.player_white = player_white
        self.player_black = player_black
        self.current_turn = 1
        self.board = board if board else chess.Board()
        self.engine = engine if engine else chess.engine.SimpleEngine.popen_uci(self.STOCKFISH_LOCATION_RPI)
        self.head = head.Head()
        self.led_manager = led_manager.LedManager()
        self.led_manager.initialize_checkerboard()
        
        threading.Thread(target=lambda: server.app.run(host="0.0.0.0", use_reloader=False)).start()
    
    def play(self):
        """The main game loop - play through each turn until a winner is determined"""
        while True:
            player = self.get_current_player()
            if (self.board.can_claim_draw()):
                print(player.name + " claims draw")
                break
            else:
                self.do_turn()
                if (self.board.is_game_over()):
                    print(player.name + " wins!")
                    break
                    
        print("Game over")

    def do_turn(self):
        """Handle a single turn for the current player"""
        player = self.get_current_player()
        move_complete = False
        while not move_complete:
            info = self.engine.analyse(self.board, chess.engine.Limit(time=0.01))
            print(info["score"])
            print(self.board)
            print(player.name + "'s turn")
            (move, requires_robot_to_move) = player.get_move(self.board, self.led_manager)
	    # TODO pass in all the current pieces' squares so we can illuminate them with the player color
            self.led_manager.initialize_checkerboard()
            if not move or not (move in self.board.legal_moves):
                print("Illegal move - try again")
            else:
                self.led_manager.illuminate_square(chess.square_name(move.from_square))
                self.led_manager.illuminate_square(chess.square_name(move.to_square), (255, 0, 0))
                is_capture = self.board.is_capture(move)
                if requires_robot_to_move:
                    # If this move was calculated by the engine or comes from a remote game, then the robot needs to move the piece
                    self.move_piece(move, is_capture)
                self.board.push(move)
                self.current_turn = self.current_turn + 1
                move_complete = True

    def get_current_player(self):
        """
        Get the Player object for the current turn
        
        :returns: Player
        """
        if (self.current_turn % 2) == 1:
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
        if (is_capture):
            print("Captured piece with type %s" % (self.board.piece_at(move.to_square).piece_type))

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
        print("Moving piece from " + str((from_column, from_row)) + " to " + str((to_column, to_row)))
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
