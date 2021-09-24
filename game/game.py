import chess
import chess.engine
import head
import game_configurator

class Game:
    def __init__(self, player_white, player_black):
        self.player_white = player_white
        self.player_black = player_black
        self.board = chess.Board()
        self.current_turn = 1
        self.game_over = False
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        self.head = head.Head()
    
    def play(self):
        while not self.board.is_game_over():
            move_complete = False
            if self.current_turn == 1:
                player = self.player_white
            else:
                player = self.player_black
            while not move_complete:
                info = self.engine.analyse(self.board, chess.engine.Limit(time=0.01))
                print(info["score"])
                print(self.board)
                print(player.name + "'s turn")
                move = player.get_move(self.board)
                if not move or not (move in self.board.legal_moves):
                    print("Illegal move")
                else:
                    self.board.push(move)
                    if not player.is_human():
                        self.move_piece(move)
                    if self.board.is_game_over():
                        print(player.name + " wins!")
                        print(self.board.result())
                        break
                    self.current_turn = (self.current_turn % 2) + 1
                    move_complete = True
        print("Game over")

    def get_coordinates_for_square(self, square):
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
        # Turn on the magnet
        self.head.set_magnet(True)
        # Move the head (and the piece) to the destination
        self.head.move_to_position(to_column, to_row)
        # Turn off the magnet
        self.head.set_magnet(False)

if __name__ == "__main__":
    configurator = game_configurator.GameConfigurator()
    game = configurator.get_game()
    game.play()
