from random import randint

class Engine():
    def __init__(self) -> None:
        self.board_width = 5
        self.board_height = 5
        self.game_board = [
            [randint(1, 3) for i in range(self.board_width)] 
            for j in range(self.board_height)
            ]

    def run(self):
        self.print_board()

    def print_board(self):
        for row in self.game_board:
            print(row)

if __name__ == '__main__':
    my_game = Engine()
    my_game.run()