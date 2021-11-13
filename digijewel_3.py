from random import randint

class Jewel():
    def __init__(self, pos) -> None:
        self.x, self.y = pos
        self.colour = randint(1, 3)
        self.reset_triples()

    def reset_triples(self):
        self.vertical_triple, self.horizontal_triple = [], []

class Engine():
    def __init__(self) -> None:
        self.board_width = 10
        self.board_height = 10
        self.game_board = [
            [Jewel((i, j)) for i in range(self.board_width)] 
            for j in range(self.board_height)
            ]

    def run(self):
        self.find_triples()
        self.print_board()

    def print_board(self):
        for row in self.game_board:
            row_jewels = []
            for jewel in row:
                row_jewels.append(jewel.colour)
            print(row_jewels)

    def find_triples(self):
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                self.game_board[i][j].reset_triples()
                if i > 0 and i < self.board_width - 1:
                    if (
                        jewel.colour == self.game_board[i - 1][j].colour and 
                        jewel.colour == self.game_board[i + 1][j].colour
                        ):
                        jewel.vertical_triple.append((i - 1, j))
                        jewel.vertical_triple.append((i, j))
                        jewel.vertical_triple.append((i + 1, j))
                if j > 0 and j < self.board_height - 1:
                    if (
                        jewel.colour == self.game_board[i][j - 1].colour and
                        jewel.colour == self.game_board[i][j + 1].colour
                        ):
                        jewel.horizontal_triple.append((i, j - 1))
                        jewel.horizontal_triple.append((i, j))
                        jewel.horizontal_triple.append((i, j + 1))
        self.clear_matched()

    def clear_matched(self):
        for row in self.game_board:
            for jewel in row:
                for cell in jewel.horizontal_triple:
                    x, y = cell
                    self.game_board[x][y].colour = 0
                for cell in jewel.vertical_triple:
                    x, y = cell
                    self.game_board[x][y].colour = 0

if __name__ == '__main__':
    my_game = Engine()
    my_game.run()