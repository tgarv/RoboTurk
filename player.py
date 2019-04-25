class Player:
    COMPUTER = 1
    HUMAN = 2
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def get_move(self):
        if self.type == self.COMPUTER:
            print("Getting move from computer player\n")
            return ""
        else:
            move = input("Enter your move:\n")
            return move