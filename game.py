import chess
import chess.engine
import player

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = chess.Board()
        self.current_turn = 1
        self.game_over = False
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
    
    def play(self):
        while not self.game_over:
            move_complete = False
            if self.current_turn == 1:
                player = self.player1
            else:
                player = self.player2
            while not move_complete:
                info = self.engine.analyse(self.board, chess.engine.Limit(time=1.00))
                print(info["score"])
                print(self.board)
                print("Player " + str(self.current_turn) + "'s turn")
                move = player.get_move(self.board)
                if not move or not (move in self.board.legal_moves):
                    print("Illegal move")
                else:
                    self.board.push(move)
                    if self.board.is_checkmate():
                        print("Player " + str(self.current_turn) + " wins!")
                        self.game_over = True
                        break
                    elif self.board.is_stalemate():
                        self.game_over = True
                        print("Stalemate!")
                        break
                    self.current_turn = (self.current_turn % 2) + 1
                    move_complete = True
        print("Game over")

if __name__ == "__main__":
    player1 = player.Player("Test1", player.Player.COMPUTER, engine_time_limit=0.001)
    player2 = player.Player("Test2", player.Player.COMPUTER, engine_time_limit=0.100)
    game = Game(player1, player2)
    game.play()