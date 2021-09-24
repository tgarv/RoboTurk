import chess
import chess.engine
import head
import game_configurator

class Game:
    def __init__(self, player_white, player_black, board = None, engine = None):
        self.player_white = player_white
        self.player_black = player_black
        self.current_turn = 1
        self.board = board if board else chess.Board()
        self.engine = engine if engine else chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        self.head = head.Head()
    
    def play(self):
        """The main game loop - play through each turn until a winner is determined"""
        while True:
            player = self.get_current_player()
            if (self.board.can_claim_draw()):
                print(player.name + " claims draw")
            else:
                self.do_turn()
                if (self.board.is_game_over()):
                    print(player.name + " wins!")
                    break
                    
        print("Game over")

    def do_turn(self):
        player = self.get_current_player()
        move_complete = False
        while not move_complete:
            info = self.engine.analyse(self.board, chess.engine.Limit(time=0.01))
            print(info["score"])
            print(self.board)
            print(player.name + "'s turn")
            (move, requires_robot_to_move) = player.get_move(self.board)
            if not move or not (move in self.board.legal_moves):
                print("Illegal move - try again")
            else:
                self.board.push(move)
                if requires_robot_to_move:
                    # If this move was calculated by the engine or comes from a remote game, then the robot needs to move the piece
                    self.move_piece(move)
                self.current_turn = self.current_turn + 1
                move_complete = True

    def get_current_player(self):
        if (self.current_turn % 2) == 1:
            return self.player_white
        return self.player_black

    def get_coordinates_for_square(self, square):
        # square is in the range (1, 64), so we need to translate that to row/column
        column = square % 8
        row = square // 8
        return (column, row)

    def move_piece(self, move):
        # TODO doesn't work for captures
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
