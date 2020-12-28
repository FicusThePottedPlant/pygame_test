import pygame
from load import *


class Board:
    # создание поля
    def __init__(self, width: int, height: int, file):
        self.width = width
        self.height = height
        self.board = list()

        self.player_pos = None

        self.level = file

        self.set_view()

    def cell_list(self):
        """get a list of cell coords of board"""
        self.board.clear()
        screen.fill('black')
        y = self.top
        a = self.cell_size
        row = []
        for _ in range(self.height):
            x = self.left
            for _ in range(self.width):
                row.append([x, y, x + a, y + a, False])
                x += a
            y += a
            self.board.append(row.copy())
            row.clear()

    # настройка внешнего вида
    def set_view(self, left=10, top=10, cell_size=30):
        """set a left, top and cell size"""
        self.left = left
        self.top = top
        self.cell_size = cell_size
        screen.fill('black')
        self.cell_list()
        for i, row in enumerate(self.level):
            for j, column in enumerate(row):
                self.put_image(i, j, column)
                self.board[i][j][-1] = column
                self.player_pos = (i, j) if column == '@' else self.player_pos

    # def render(self):
    #     """render a board"""
    #     y = self.top
    #     a = self.cell_size
    #     for _ in range(self.height):
    #         x = self.left
    #         for _ in range(self.width):
    #             pygame.draw.rect(screen, 'white', (x, y, a, a), True)
    #             x += a
    #         y += a
    #     self.update()

    def get_cell(self, mouse_pos: tuple) -> tuple:
        """get cell coord by clicking on it"""
        for i, row in enumerate(self.board):
            for j, coord in enumerate(row):
                x, y, x1, y1, _ = coord
                if x <= mouse_pos[0] <= x1 and y <= mouse_pos[1] <= y1:
                    return i, j

    def get_click(self, mouse_pos: tuple):
        """handle get_cell and on_click"""
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def on_click(self, cell_coord: tuple):
        """do something with a clicked cell"""
        i, j = cell_coord

    def put_image(self, x, y, image):
        x, y = self.board[x][y][:2]
        Tile(x, y, image)

    def update(self):
        to_x, to_y = self.player_pos
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_UP]:
                to_x -= 1
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                to_x += 1
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                to_y -= 1
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                to_y += 1

        if self.player_pos and self.board[to_x][to_y][-1] != '#':
            self.put_image(self.player_pos[0], self.player_pos[1], '.')
            game.player_pos = to_x, to_y
            self.put_image(*self.player_pos, '$')


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, type_of_tile):
        super().__init__(all_sprites)
        tile_images = {
            '#': load_image('box.png'),
            '.': load_image('grass.png'),
            '@': load_image('grass.png'),
            '$': load_image('mar.png')
        }
        self.image = tile_images[type_of_tile]
        self.image = pygame.transform.smoothscale(self.image,
                                                  (500 // len(file),
                                                   500 // len(file))) if type_of_tile != '$' else self.image
        self.status = type_of_tile
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def get_status(self):
        return self.status


my_level = input()
try:
    file = load_level(my_level)
except FileNotFoundError:
    exit(print('File not found'))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.smoothscale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_screen()
    running = True
    all_sprites = pygame.sprite.Group()
    fps = 10
    game = Board(len(file), len(file[0]), file)
    game.set_view(0, 0, 500 // len(file))

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            game.update()
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
