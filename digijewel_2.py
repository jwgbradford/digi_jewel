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
        self.find_triples()
        self.print_board()

    def print_board(self):
        for row in self.game_board:
            print(row)

    def find_triples(self):
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                if i > 0 and i < self.board_width - 1:
                    if (
                        jewel == self.game_board[i - 1][j] and 
                        jewel == self.game_board[i + 1][j]
                        ):
                        self.game_board[i][j] = 0
                        self.game_board[i - 1][j] = 0
                        self.game_board[i + 1][j] = 0
                if j > 0 and j < self.board_height - 1:
                    if (
                        jewel == self.game_board[i][j - 1] and
                        jewel == self.game_board[i][j + 1]
                        ):
                        self.game_board[i][j] = 0
                        self.game_board[i][j - 1] = 0
                        self.game_board[i][j + 1] = 0


if __name__ == '__main__':
    my_game = Engine()
    my_game.run()