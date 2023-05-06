import sys
import pygame as pg
from settings import *
from board import Board
from figures import Figures


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()

        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_map_pos = int((self.mouse_pos[1] - FRAME_SIZE) / FIELD_SIZE), int(
            (self.mouse_pos[0] - FRAME_SIZE) / FIELD_SIZE)

        self.highlighted_fields = None
        self.possible_moves = None
        self.check_tile = None
        self.turns = 0
        self.turn_history = {}

        self.board = Board(self)
        self.figures = Figures(self)

    def update(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_map_pos = int((self.mouse_pos[1] - FRAME_SIZE) / FIELD_SIZE), int(
            (self.mouse_pos[0] - FRAME_SIZE) / FIELD_SIZE)

        self.figures.update()

        pg.display.set_caption('CHESS')
        pg.display.flip()
        self.clock.tick(60)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                for figure in self.figures.figures_list:
                    if figure.rect.collidepoint(event.pos) and self.turn == figure.color:
                        self.highlighted_fields = [figure.get_pos]
                        self.possible_moves = figure.get_possible_moves
                        break
                    elif self.possible_moves and self.mouse_map_pos in self.possible_moves \
                            and figure.get_pos in self.highlighted_fields:
                        figure.move(self.mouse_map_pos)
                        self.highlighted_fields.append(figure.get_pos)
                        self.possible_moves = None

    @property
    def turn(self):
        if self.turns % 2 == 0:
            return 'white'
        else:
            return 'black'

    @property
    def check(self):
        check_color = None
        danger_tiles = self.board.danger_tiles
        for figure in self.figures.figures_list:
            if figure.figure == 'king':
                if figure.get_pos in danger_tiles.get(figure.color):
                    self.check_tile = figure.get_pos
                    self.checkmate(figure)
                    check_color = figure.color
                    break
        if not check_color:
            self.check_tile = None

        return check_color

    def checkmate(self, king):
        if king.get_possible_moves:
            return

        attacking_tile = False
        attacking_figure = False
        danger_tiles_by_pos = self.board.danger_tiles_by_pos

        for color in danger_tiles_by_pos:
            if color == king.color:
                continue
            for pos in danger_tiles_by_pos.get(color):
                if king.get_pos in danger_tiles_by_pos.get(color).get(pos):
                    attacking_tile = pos

        for figure in self.figures.figures_list:
            if figure.get_pos == attacking_tile:
                attacking_figure = figure

        for figure in self.figures.figures_list:
            if figure.color != king.color:
                continue
            for pos in figure.get_possible_moves:
                if pos == attacking_tile:
                    return
                if king.get_pos not in figure.move(pos=pos, test=True, figure=attacking_figure):
                    return

        print('Checkmate')

    def draw(self):
        self.board.draw(self.highlighted_fields, self.possible_moves, self.mouse_map_pos)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
