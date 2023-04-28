from settings import *
import pygame as pg


class Figures:
    def __init__(self, game):
        self.game = game
        self.figures_list = []

        self.create_figures()

    def create_figures(self):
        add_figure = self.add_figure

        for color in ['white', 'black']:
            [add_figure(Pawn(self.game, 'pawn', color, (6 if color == 'white' else 1, col))) for col in range(0, 8)]
            row = 7 if color == 'white' else 0
            [add_figure(Rook(self.game, 'rook', color, (row, col))) for col in [0, 7]]
            [add_figure(Knight(self.game, 'knight', color, (row, col))) for col in [1, 6]]
            [add_figure(Bishop(self.game, 'bishop', color, (row, col))) for col in [2, 5]]
            add_figure(Queen(self.game, 'queen', color, (row, 3)))
            add_figure(King(self.game, 'king', color, (row, 4)))

        [self.game.board.figures_map.update({figure.get_pos: figure.color}) for figure in self.figures_list]

    def update(self):
        [figure.update() for figure in self.figures_list]

    def add_figure(self, figure):
        self.figures_list.append(figure)


class Figure:
    def __init__(self, game, figure, color, pos):
        self.game = game
        self.screen = game.screen
        self.figures_map = game.board.figures_map
        self.figure = figure
        self.color = color
        self.image = pg.image.load(f'graphics/figures/{figure}-{color}.png').convert_alpha()
        self.row, self.col = pos
        self.start_pos = True
        self.img_rect = self.image.get_rect(center=(FRAME_SIZE + self.col * FIELD_SIZE + FIELD_SIZE / 2,
                                                    FRAME_SIZE + self.row * FIELD_SIZE + FIELD_SIZE / 2))
        self.rect = pg.rect.Rect(self.col * FIELD_SIZE + FRAME_SIZE, self.row * FIELD_SIZE + FRAME_SIZE,
                                 FIELD_SIZE, FIELD_SIZE)
        self.highlighted = False

    def move(self, pos):
        previous_pos = self.row, self.col
        self.figures_map.update({pos: self.color})
        self.figures_map.pop(previous_pos)
        self.row, self.col = pos
        if self.start_pos:
            self.start_pos = False
        self.check_collision()
        self.img_rect = self.image.get_rect(center=(FRAME_SIZE + self.col * FIELD_SIZE + FIELD_SIZE / 2,
                                                    FRAME_SIZE + self.row * FIELD_SIZE + FIELD_SIZE / 2))
        self.rect = pg.rect.Rect(self.col * FIELD_SIZE + FRAME_SIZE, self.row * FIELD_SIZE + FRAME_SIZE,
                                 FIELD_SIZE, FIELD_SIZE)

        if self.figure == 'king' and self.row in [0, 7] and self.col in [2, 6]:
            self.castling((self.row, 7 if self.col == 6 else 0))
            return
        elif self.row in [0, 7] and self.figure == 'pawn':
            self.upgrade_to_queen()

        self.game.turns += 1

        self.game.turn_history.update({
            self.game.turns: f'{self.game.board.letters[previous_pos[1]]}{self.game.board.nums[-previous_pos[0] - 1]}'
                             f' ->{self.game.board.letters[self.col]}{self.game.board.nums[-self.row - 1]}'
        })

    def check_collision(self):
        for figure in self.game.figures.figures_list:
            if figure.get_pos == self.get_pos and figure.color != self.color:
                index = [i for i in self.game.figures.figures_list].index(figure)
                self.game.figures.figures_list.pop(index)
                if self.figures_map.get(self.get_pos) != self.color:
                    self.figures_map.pop(self.get_pos)

    def castling(self, pos):
        for figure in self.game.figures.figures_list:
            if figure.figure == 'rook' and figure.color == self.color and figure.get_pos == pos:
                figure.move((self.row, 5 if pos[1] == 7 else 3))

    def upgrade_to_queen(self):
        self.game.figures.add_figure(Queen(self.game, 'queen', self.color, self.get_pos))
        self.game.figures.figures_list.remove(self)

    @property
    def get_pos(self):
        return self.row, self.col

    def draw(self):
        self.screen.blit(self.image, self.img_rect)

    def update(self):
        self.draw()


class Pawn(Figure):
    def __init__(self, game, figure, color, pos):
        super().__init__(game, figure, color, pos)

    @property
    def get_possible_moves(self):
        moves = []
        next_row = self.row + self.move_direction(1)

        if (next_row, self.col) not in self.figures_map:
            moves.append((next_row, self.col))
            if self.start_pos and (self.row + self.move_direction(2), self.col) not in self.figures_map:
                moves.append((self.row + self.move_direction(2), self.col))

        [moves.append((next_row, self.col + 1 * i))
         for i in [-1, 1] if (next_row, self.col + 1 * i) in self.figures_map and
         self.figures_map.get((next_row, self.col + 1 * i)) != self.color]

        return moves

    def move_direction(self, value):
        return -value if self.color == 'white' else value

    @property
    def get_dangerous_moves(self):
        return [(self.row + self.move_direction(1), self.col + 1), (self.row + self.move_direction(1), self.col - 1)]


class Rook(Figure):
    def __init__(self, game, figure, color, pos):
        super().__init__(game, figure, color, pos)

    @property
    def get_possible_moves(self):
        moves = []

        left, right, up, down = [], [], [], []

        for i in range(1, 8):
            left.append((self.row, self.col - i))
            right.append((self.row, self.col + i))
            up.append((self.row + i, self.col))
            down.append((self.row - i, self.col))

        for direction in [left, right, up, down]:
            for pos in direction:
                if pos in self.figures_map:
                    if self.figures_map.get(pos) != self.color:
                        moves.append(pos)
                    break
                moves.append(pos)

        return moves

    @property
    def get_dangerous_moves(self):
        return self.get_possible_moves


class Knight(Figure):
    def __init__(self, game, figure, color, pos):
        super().__init__(game, figure, color, pos)

    @property
    def get_possible_moves(self):
        moves = [(self.row + x, self.col + y)
                 for x, y in [(-2, 1), (-2, -1), (2, 1), (2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
                 if self.figures_map.get((self.row + x, self.col + y)) != self.color]

        return moves

    @property
    def get_dangerous_moves(self):
        return self.get_possible_moves


class Bishop(Figure):
    def __init__(self, game, figure, color, pos):
        super().__init__(game, figure, color, pos)

    @property
    def get_possible_moves(self):
        moves = []

        for x, y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for i in range(1, 8):
                pos = (self.row + x * i, self.col + y * i)
                if pos in self.figures_map:
                    if self.figures_map.get(pos) != self.color:
                        moves.append(pos)
                    break
                moves.append(pos)

        return moves

    @property
    def get_dangerous_moves(self):
        return self.get_possible_moves


class Queen(Figure):
    def __init__(self, game, figure, color, pos):
        super().__init__(game, figure, color, pos)

    @property
    def get_possible_moves(self):
        moves = []

        left, right, up, down = [], [], [], []

        for i in range(1, 8):
            left.append((self.row, self.col - i))
            right.append((self.row, self.col + i))
            up.append((self.row + i, self.col))
            down.append((self.row - i, self.col))

        for direction in [left, right, up, down]:
            for pos in direction:
                if pos in self.figures_map:
                    if self.figures_map.get(pos) != self.color:
                        moves.append(pos)
                    break
                moves.append(pos)

        for x, y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for i in range(1, 8):
                pos = (self.row + x * i, self.col + y * i)
                if pos in self.figures_map:
                    if self.figures_map.get(pos) != self.color:
                        moves.append(pos)
                    break
                moves.append(pos)

        return moves

    @property
    def get_dangerous_moves(self):
        return self.get_possible_moves


class King(Figure):
    def __init__(self, game, figure, color, pos):
        super().__init__(game, figure, color, pos)

    @property
    def get_possible_moves(self):
        moves = [(self.row + x, self.col + y) for x, y in
                 [(0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1), (1, 1), (1, 0), (1, -1)]
                 if self.figures_map.get((self.row + x, self.col + y)) != self.color
                 and self.row + x in range(0, 8) and self.col + y in range(0, 8)
                 and (self.row + x, self.col + y) not in self.game.board.danger_tiles.get(self.color)]

        if self.start_pos and (self.row, self.col + 1) not in self.figures_map and\
                (self.row, self.col + 2) not in self.figures_map:
            for figure in self.game.figures.figures_list:
                if figure.figure == 'rook' and figure.get_pos == (self.row, self.col + 3) and figure.start_pos:
                    moves.append((self.row, self.col + 2))

        if self.start_pos and (self.row, self.col - 1) not in self.figures_map and\
                (self.row, self.col - 2) not in self.figures_map and (self.row, self.col - 3) not in self.figures_map:
            for figure in self.game.figures.figures_list:
                if figure.figure == 'rook' and figure.get_pos == (self.row, self.col - 4) and figure.start_pos:
                    moves.append((self.row, self.col - 2))

        return moves

    @property
    def get_dangerous_moves(self):
        moves = [(self.row + x, self.col + y) for x, y in
                 [(0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1), (1, 1), (1, 0), (1, -1)]
                 if self.figures_map.get((self.row + x, self.col + y)) != self.color
                 and self.row + x in range(0, 8) and self.col + y in range(0, 8)
                 and (self.row + x, self.col + y)]

        return moves
