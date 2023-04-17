from settings import *
import pygame as pg


chess_figures = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn',
                 'rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']


class Figures:
    def __init__(self, game):
        self.game = game
        self.figures_list = []
        self.chess_figures = chess_figures
        add_figure = self.add_figure

        pos = [6, 0]
        for color in ['white', 'black']:
            if color == 'black':
                self.chess_figures = chess_figures[::-1]
                pos = [0, 0]
            for figure in self.chess_figures:
                add_figure(Figure(game, figure, color, pos))
                pos[1] += 1
                if pos[1] > 7:
                    pos[0] += 1
                    pos[1] = 0

    def update(self):
        [figure.update() for figure in self.figures_list]

    def add_figure(self, figure):
        self.figures_list.append(figure)


class Figure:
    def __init__(self, game, figure, color, pos):
        self.game = game
        self.screen = game.screen
        self.figure = figure
        self.color = color
        self.image = pg.image.load(f'graphics/figures/{figure}-{color}.png').convert_alpha()
        self.row, self.col = pos
        self.start_pos = self.row, self.col
        self.img_rect = self.image.get_rect(center=(FRAME_SIZE + self.col * FIELD_SIZE + FIELD_SIZE / 2,
                                                    FRAME_SIZE + self.row * FIELD_SIZE + FIELD_SIZE / 2))
        self.rect = pg.rect.Rect(self.col * FIELD_SIZE + FRAME_SIZE, self.row * FIELD_SIZE + FRAME_SIZE,
                                 FIELD_SIZE, FIELD_SIZE)
        self.highlighted = False

    def move(self, pos):
        self.game.board.figures_map[self.row][self.col] = 0
        self.row, self.col = pos
        self.check_collision()
        self.game.board.figures_map[self.row][self.col] = 1
        self.img_rect = self.image.get_rect(center=(FRAME_SIZE + self.col * FIELD_SIZE + FIELD_SIZE / 2,
                                                    FRAME_SIZE + self.row * FIELD_SIZE + FIELD_SIZE / 2))
        self.rect = pg.rect.Rect(self.col * FIELD_SIZE + FRAME_SIZE, self.row * FIELD_SIZE + FRAME_SIZE,
                                 FIELD_SIZE, FIELD_SIZE)

        self.game.turns += 1

    def check_collision(self):
        for figure in self.game.figures.figures_list:
            if figure.get_pos == self.get_pos and figure.color != self.color:
                index = [i for i in self.game.figures.figures_list].index(figure)
                self.game.figures.figures_list.pop(index)

    def move_direction(self, value):
        if self.color == 'white':
            return -value
        else:
            return value

    @property
    def get_possible_moves(self):
        if self.figure == 'pawn':
            if self.start_pos == self.get_pos:
                return (self.row + self.move_direction(1), self.col), (self.row + self.move_direction(2), self.col)
            else:
                return (self.row + self.move_direction(1), self.col), None

    @property
    def get_pos(self):
        return self.row, self.col

    def draw(self):
        self.screen.blit(self.image, self.img_rect)

    def update(self):
        self.draw()
