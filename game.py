from random import randint
import pygame

COLOURS = [ (0, 0, 0),
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 255), (255, 0, 255),
    ]

holding = [
    (0, 191, 255), (0, 128, 255), 
    (0, 64, 255), (191, 255, 0), 
    (255, 191, 0), 
    (0, 255, 64), (0, 255, 128), (0, 255, 191),
    (128, 255, 0), (64, 255, 0), (255, 64, 0), (255, 128, 0), 
    ]

TEST_BOARD = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [2, 3, 4, 5, 6, 7, 8, 9, 11, 12],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [2, 3, 4, 5, 6, 7, 8, 9, 11, 12],
    [2, 3, 4, 5, 6, 7, 8, 9, 11, 12],
    [3, 4, 5, 6, 7, 8, 9, 11, 12, 13],
    [2, 4, 3, 6, 7, 8, 9, 11, 12, 13],
    [4, 4, 4, 5, 6, 7, 8, 9, 10, 11],
    [3, 4, 5, 6, 7, 8, 9, 11, 12, 13],
    [3, 4, 5, 6, 7, 8, 9, 11, 12, 13]
]

class Jewel():
    def __init__(self, pos) -> None:
        self.x, self.y = pos
        self.colour = randint(1, len(COLOURS) - 1)
        self.update_jewel()
        self.reset_triples()

    def update_jewel (self):
        self.make_image()
        self.get_rect()

    def reset_triples(self):
        self.vertical_triple, self.horizontal_triple = [], []
        
    def make_image(self):
        image = pygame.Surface((40, 40))
        image.set_colorkey(COLOURS[0])  # Black colors will not be blit.
        pygame.draw.circle(image, COLOURS[self.colour], (20, 20), 20)
        self.my_image =  image

    def fade_image(self, rgb):
        image = pygame.Surface((40, 40))
        image.set_colorkey(COLOURS[0])  # Black colors will not be blit.
        pygame.draw.circle(image, rgb, (20, 20), 20)
        self.my_image =  image

    def get_rect(self):
        jewel_center = (20 + (self.x * 40), 20 + (self.y * 40))
        jewel_rect = self.my_image.get_rect(center = jewel_center)
        self.my_rect =  jewel_rect

    def reset_image(self):
        self.make_image()
        self.get_rect()

    def drop_rect(self, dy):
        jewel_center = (20 + (self.x * 40), 20 + ((self.y * 40) + dy))
        jewel_rect = self.my_image.get_rect(center = jewel_center)
        self.my_rect =  jewel_rect

    def slide_rect(self, step, dirx, diry):
        dx = step * dirx
        dy = step * diry
        jewel_center = (20 + (self.x * 40) + dx, 20 + ((self.y * 40) + dy))
        jewel_rect = self.my_image.get_rect(center = jewel_center)
        self.my_rect =  jewel_rect

class Engine():
    def __init__(self) -> None:
        self.board_width = 10
        self.board_height = 10
        pygame.init()
        self.game_window = pygame.display.set_mode((self.board_width * 40 + 120, self.board_height * 40))
        pygame.display.set_caption("DigiJewels")
        self.font = pygame.font.SysFont('arial', 40)
        self.score_label = self.font.render("Score", True, (175, 175, 175))
        self.game_board = [[Jewel((i, j)) for i in range(self.board_width)] for j in range(self.board_height)]
        #self.setup_test()
        self.first_pos = self.second_pos = (-1 ,-1)
        self.score = 0

    def setup_test(self):
        for i, row in enumerate(TEST_BOARD):
            for j, colour in enumerate(row):
                self.game_board[i][j].colour = colour
                self.game_board[i][j].update_jewel()

    def pos_to_coord(self):
        pos = pygame.mouse.get_pos()
        row, col = pos[1]//40, pos[0]//40
        return (row, col)

    def run(self):
        while True:
            self.find_triples()
            self.draw_board()
            self.board_drop()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.first_pos == (-1, -1):
                        self.first_pos = self.pos_to_coord()
                    else:
                        self.second_pos = self.pos_to_coord()
                        self.jewel_swap()
                if event.type == pygame.QUIT:
                    pygame.quit()

    def column_drop(self, i):
        columns_to_drop = {}
        # test if any columns contain black jewels
        for j in range(self.board_width):
            if self.game_board[i][j].colour == 0:
                row_drop_count = 0
                if i == 0:
                    self.game_board[i][j].colour = randint(1, len(COLOURS) - 1) # make a new jewel
                    self.game_board[i][j].reset_image()
                else:
                    for x in range(i):
                        if self.game_board[0][j].colour == 0:
                            self.game_board[0][j].colour = randint(1, len(COLOURS) - 1) # make a new jewel
                            self.game_board[0][j].reset_image()
                        if self.game_board[i - x][j].colour == 0: # if the jewel above ours is also black, we keep going
                            row_drop_count += 1
                    columns_to_drop[j] = row_drop_count
        return columns_to_drop

    def jewel_drop(self, i, columns_to_drop):
        for dy in range(40):
            for column in columns_to_drop:
                rows_to_drop = columns_to_drop[column]
                if rows_to_drop > 0:
                    if self.game_board[0][column].colour == 0:
                        self.game_board[0][column].colour = randint(1, len(COLOURS) - 1) # make a new jewel
                        self.game_board[0][column].reset_image()
                    for dx in range(i - rows_to_drop + 1):
                        self.game_board[i - rows_to_drop - dx][column].drop_rect(dy)
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.time.Clock().tick(60)

    def drop_rows(self, i, columns_to_drop):
        max_drop = 1
        for column in columns_to_drop:
            if columns_to_drop[column] > max_drop:
                max_drop = columns_to_drop[column]
        for _ in range(max_drop):
            self.jewel_drop(i, columns_to_drop)
            for column in columns_to_drop:
                if columns_to_drop[column] > 0:
                    rows_to_drop = columns_to_drop[column]
                    for dx in range(i - rows_to_drop + 1):
                        self.game_board[i - rows_to_drop + 1 - dx][column].colour = self.game_board[i - rows_to_drop - dx][column].colour
                        self.game_board[i - rows_to_drop + 1 - dx][column].reset_image()
                        self.game_board[i - rows_to_drop - dx][column].colour = 0
                        self.game_board[i - rows_to_drop - dx][column].reset_image()
                    columns_to_drop[column] -= 1

    def board_drop(self):
        # to drop the board, we want to start at the bottom row, and work up
        for i in range(self.board_height - 1, -1, -1):
            columns_to_drop = self.column_drop(i)
            if len(columns_to_drop) > 0:
                self.drop_rows(i, columns_to_drop)

    def jewel_swap(self):
        dy = self.first_pos[0] - self.second_pos[0]
        dx = self.first_pos[1] - self.second_pos[1]
        if (
            ((abs(dx) == 1) and dy == 0 ) != 
            (dx == 0 and (abs(dy) == 1) )
            ):
            for step in range(40):
                self.game_board[self.first_pos[0]][self.first_pos[1]].slide_rect(step, -dx, -dy)
                self.game_board[self.second_pos[0]][self.second_pos[1]].slide_rect(step, dx, dy)
                self.draw_board()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                pygame.time.Clock().tick(60)
            first_colour = self.game_board[self.first_pos[0]][self.first_pos[1]].colour
            self.game_board[self.first_pos[0]][self.first_pos[1]].colour = self.game_board[self.second_pos[0]][self.second_pos[1]].colour
            self.game_board[self.first_pos[0]][self.first_pos[1]].reset_image()
            self.game_board[self.second_pos[0]][self.second_pos[1]].colour = first_colour
            self.game_board[self.second_pos[0]][self.second_pos[1]].reset_image()

    def find_triples(self):
        no_triples = True
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                self.game_board[i][j].reset_triples()
                if i > 0 and i < self.board_width - 1:
                    if (
                        jewel.colour == self.game_board[i - 1][j].colour and 
                        jewel.colour == self.game_board[i + 1][j].colour
                        ):
                        jewel.vertical_triple.append((i, j))
                        jewel.vertical_triple.append((i - 1, j))
                        jewel.vertical_triple.append((i + 1, j))
                        self.score += 1
                        no_triples = False
                if j > 0 and j < self.board_height - 1:
                    if (
                        jewel.colour == self.game_board[i][j - 1].colour and
                        jewel.colour == self.game_board[i][j + 1].colour
                        ):
                        jewel.vertical_triple.append((i, j))
                        jewel.horizontal_triple.append((i, j - 1))
                        jewel.horizontal_triple.append((i, j + 1))
                        self.score += 1
                        no_triples = False
        if no_triples and self.first_pos != (-1, -1) and self.second_pos != (-1, -1):
            self.undo_move()
        elif not no_triples:
            self.first_pos = self.second_pos = (-1 ,-1)
        self.clear_matched()

    def undo_move(self):
        temp_pos = self.first_pos
        self.first_pos = self.second_pos
        self.second_pos = temp_pos
        self.jewel_swap()
        self.first_pos = self.second_pos = (-1, -1)

    def clear_matched(self):
        jewel_fade = []
        for i, row in enumerate(self.game_board):
            for j, jewel in enumerate(row):
                if len(jewel.horizontal_triple) > 0:
                    for cell in jewel.horizontal_triple:
                        if cell not in jewel_fade:
                            jewel_fade.append(cell)
                if len(jewel.vertical_triple) > 0:
                    for cell in jewel.vertical_triple:
                        if cell not in jewel_fade:
                            jewel_fade.append(cell)
        if len(jewel_fade) > 0:
            self.fade(jewel_fade)

    def fade(self, jewels_to_fade):
        jewel_colours = [COLOURS[self.game_board[cell[0]][cell[1]].colour] for cell in jewels_to_fade]
        #input(jewel_colours)
        for _ in range(51):
            for colour_index, cell in enumerate(jewels_to_fade):
                x, y = cell
                r, g, b  = jewel_colours[colour_index]
                if r > 4:
                    r -= 5
                else:
                    r = 0
                if g > 4:
                    g -= 5
                else:
                    g = 0
                if b > 4:
                    b -= 5
                else:
                    b = 0
                self.game_board[x][y].fade_image((r, g, b))
                jewel_colours[colour_index] = (r, g, b)
            self.draw_board()
            pygame.time.Clock().tick(60)
        for cell in jewels_to_fade:
            self.game_board[cell[0]][cell[1]].colour = 0 

    def draw_board(self):
        self.game_window.fill(COLOURS[0])
        for row in self.game_board:
            for jewel in row:
                self.game_window.blit(jewel.my_image, jewel.my_rect)
        self.game_window.blit(self.score_label, (410,80))
        score_text = self.font.render(str(self.score), True, (175, 175, 175))
        self.game_window.blit(score_text, (440,120))
        pygame.display.update()

    def print_board(self):
        for row in self.game_board:
            row_jewels = []
            for jewel in row:
                row_jewels.append(jewel.colour)
            print(row_jewels)

if __name__ == '__main__':
    my_game = Engine()
    my_game.run()