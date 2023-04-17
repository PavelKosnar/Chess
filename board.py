import pygame as pg
from settings import *

board = [
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0]
]

figures_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

letters = 'abcdefgh'
nums = '12345678'


class Board:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.board = board
        self.font = pg.font.Font(pg.font.get_default_font(), int(min(WIDTH, HEIGHT) / 35))
        self.figures_map = figures_map

    def draw(self, highlight=None, pointed_fields=None, mouse_pos=None):
        self.screen.fill((33, 33, 33))
        for row, items in enumerate(self.board):
            for col, field in enumerate(items):
                if row == 0:
                    self.screen.blit(self.font.render(letters[col], False, 'White'),
                                     (FRAME_SIZE / 1.5 + col * FIELD_SIZE + FIELD_SIZE / 2, 0))
                elif row == 7:
                    self.screen.blit(self.font.render(letters[col], False, 'White'),
                                     (FRAME_SIZE / 1.5 + col * FIELD_SIZE + FIELD_SIZE / 2, HEIGHT - FRAME_SIZE))

                if col == 0:
                    self.screen.blit(self.font.render(nums[-row - 1], False, 'White'),
                                     (FRAME_SIZE / 4, FRAME_SIZE / 1.5 + row * FIELD_SIZE + FIELD_SIZE / 2))
                elif col == 7:
                    self.screen.blit(self.font.render(nums[-row - 1], False, 'White'),
                                     (WIDTH - FRAME_SIZE / 1.2, FRAME_SIZE / 1.5 + row * FIELD_SIZE + FIELD_SIZE / 2))

                if highlight and (col, row) in highlight:
                    pg.draw.rect(self.screen, '#f9b71c', (row * FIELD_SIZE + FRAME_SIZE, col * FIELD_SIZE + FRAME_SIZE,
                                                          FIELD_SIZE, FIELD_SIZE))
                    continue

                if field == 1:
                    pg.draw.rect(self.screen, '#d18b47', (row * FIELD_SIZE + FRAME_SIZE, col * FIELD_SIZE + FRAME_SIZE,
                                                          FIELD_SIZE, FIELD_SIZE))
                elif field == 0:
                    pg.draw.rect(self.screen, '#ffce9e', (row * FIELD_SIZE + FRAME_SIZE, col * FIELD_SIZE + FRAME_SIZE,
                                                          FIELD_SIZE, FIELD_SIZE))

                if pointed_fields and (col, row) in pointed_fields:
                    surface = pg.Surface((FIELD_SIZE, FIELD_SIZE), pg.SRCALPHA)
                    if mouse_pos == (col, row) and mouse_pos in pointed_fields:
                        pg.draw.rect(surface, (255, 200, 132, 150), (0, 0, FIELD_SIZE, FIELD_SIZE))
                    else:
                        pg.draw.circle(surface, (33, 33, 33, 150), (FIELD_SIZE / 2 + 1, FIELD_SIZE / 2 + 1), WIDTH / 60)
                    self.screen.blit(surface, (row * FIELD_SIZE + FRAME_SIZE, col * FIELD_SIZE + FRAME_SIZE))
