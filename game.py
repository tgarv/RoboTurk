import chess
import chess.engine
import player

class Game:
    def __init__(self, player_white, player_black):
        self.player_white = player_white
        self.player_black = player_black
        self.board = chess.Board()
        self.current_turn = 1
        self.game_over = False
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
    
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
                    if self.board.is_game_over():
                        print(player.name + " wins!")
                        print(self.board.result())
                        break
                    self.current_turn = (self.current_turn % 2) + 1
                    move_complete = True
        print("Game over")

if __name__ == "__main__":
    player1 = player.Player("White", player.Player.COMPUTER, engine_time_limit=0.001)
    player2 = player.Player("Black", player.Player.COMPUTER, engine_time_limit=0.001)
    game = Game(player1, player2)
    game.play()