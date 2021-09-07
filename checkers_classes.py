import pygame
import os

WIN_SIZE = 800, 800
WIN = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("Checkers")

TILE_SIZE = WIN_SIZE[0] / 8, WIN_SIZE[1] / 8

WHITE_PIECE_IMG = pygame.image.load(os.path.join("Assets", "white_piece.png")).convert()
WHITE_PIECE_IMG.set_colorkey("white")
BLACK_PIECE_IMG = pygame.image.load(os.path.join("Assets", "black_piece.png")).convert()
BLACK_PIECE_IMG.set_colorkey("white")
CLEAR_WHITE_PIECE_IMG = pygame.image.load(
    os.path.join("Assets", "clear_white_piece.png")
).convert_alpha()
CLEAR_WHITE_PIECE_IMG.set_colorkey("white")
CLEAR_BLACK_PIECE_IMG = pygame.image.load(
    os.path.join("Assets", "clear_black_piece.png")
).convert_alpha()
CLEAR_BLACK_PIECE_IMG.set_colorkey("white")

board = [[None for _ in range(8)] for _ in range(8)]


def board_to_coords(x, y):
    # Convert coordinates on the board to coordinates of the display (e.g. 2, 3 to 200, 400)
    ratio = WIN_SIZE[0] / 8
    x = x * ratio
    y = y * ratio
    return x, y


class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((board_to_coords(self.x, self.y), (TILE_SIZE)))

    def set_pos(self, x, y):
        board[self.y][self.x] = None
        self.x = x
        self.y = y
        board[self.y][self.x] = self
        self.rect.topleft = board_to_coords(x, y)

    def collide(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False


class White(Piece):
    instances = []

    def __init__(self, x, y):
        super().__init__(x, y)
        self.__class__.instances.append(self)

    def find_valid(self):
        valid_moves = []
        try:
            if self.y - 1 < 0:
                raise IndexError
            if board[self.y - 1][self.x + 1] == None:
                valid_moves.append({"coords": (self.x + 1, self.y - 1)})
            elif (
                type(board[self.y - 1][self.x + 1]) == Black
                and board[self.y - 2][self.x + 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x + 2, self.y - 2),
                        "cap_piece": board[self.y - 1][self.x + 1],
                    }
                )
        except IndexError:
            pass
        try:
            if self.y < 0 or self.x < 0:
                raise IndexError
            if board[self.y - 1][self.x - 1] == None:
                valid_moves.append({"coords": (self.x - 1, self.y - 1)})
            elif (
                type(board[self.y - 1][self.x - 1]) == Black
                and board[self.y - 2][self.x - 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x - 2, self.y - 2),
                        "cap_piece": board[self.y - 1][self.x - 1],
                    }
                )
        except IndexError:
            pass
        return valid_moves

    def second_cap(self):
        valid_moves = []
        try:
            if self.y - 2 < 0:
                raise IndexError
            if (
                type(board[self.y - 1][self.x + 1]) == Black
                and board[self.y - 2][self.x + 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x + 2, self.y - 2),
                        "cap_piece": board[self.y - 1][self.x + 1],
                    }
                )
        except IndexError:
            pass
        try:
            if self.y - 2 < 0 or self.x - 2 < 0:
                raise IndexError
            if (
                type(board[self.y - 1][self.x - 1]) == Black
                and board[self.y - 2][self.x - 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x - 2, self.y - 2),
                        "cap_piece": board[self.y - 1][self.x - 1],
                    }
                )
        except IndexError:
            pass
        try:
            if (
                type(board[self.y + 1][self.x + 1]) == Black
                and board[self.y + 2][self.x + 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x + 2, self.y + 2),
                        "cap_piece": board[self.y + 1][self.x + 1],
                    }
                )
        except IndexError:
            pass
        try:
            if self.x - 2 < 0:
                raise IndexError
            if (
                type(board[self.y + 1][self.x - 1]) == Black
                and board[self.y + 2][self.x - 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x - 2, self.y + 2),
                        "cap_piece": board[self.y + 1][self.x - 1],
                    }
                )
        except IndexError:
            pass
        return valid_moves

    def draw(self):
        WIN.blit(WHITE_PIECE_IMG, board_to_coords(self.x, self.y))


class Black(Piece):
    instances = []

    def __init__(self, x, y):
        super().__init__(x, y)
        self.__class__.instances.append(self)

    def find_valid(self):
        valid_moves = []
        try:
            if board[self.y + 1][self.x + 1] == None:
                valid_moves.append({"coords": (self.x + 1, self.y + 1)})
            elif (
                type(board[self.y + 1][self.x + 1]) == White
                and board[self.y + 2][self.x + 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x + 2, self.y + 2),
                        "cap_piece": board[self.y + 1][self.x + 1],
                    }
                )
        except IndexError:
            pass
        try:
            if self.x < 0:
                raise IndexError
            if board[self.y + 1][self.x - 1] == None:
                valid_moves.append({"coords": (self.x - 1, self.y + 1)})
            elif (
                type(board[self.y + 1][self.x - 1]) == White
                and board[self.y + 2][self.x - 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x - 2, self.y + 2),
                        "cap_piece": board[self.y + 1][self.x - 1],
                    }
                )
        except IndexError:
            pass
        return valid_moves

    def second_cap(self):
        valid_moves = []
        try:
            if self.y - 2 < 0:
                raise IndexError
            if (
                type(board[self.y - 1][self.x + 1]) == White
                and board[self.y - 2][self.x + 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x + 2, self.y - 2),
                        "cap_piece": board[self.y - 1][self.x + 1],
                    }
                )
        except IndexError:
            pass
        try:
            if self.y < 0 or self.x < 0:
                raise IndexError
            if (
                type(board[self.y - 1][self.x - 1]) == White
                and board[self.y - 2][self.x - 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x - 2, self.y - 2),
                        "cap_piece": board[self.y - 1][self.x - 1],
                    }
                )
        except IndexError:
            pass
        try:
            if (
                type(board[self.y + 1][self.x + 1]) == White
                and board[self.y + 2][self.x + 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x + 2, self.y + 2),
                        "cap_piece": board[self.y + 1][self.x + 1],
                    }
                )
        except IndexError:
            pass
        try:
            if self.x < 0:
                raise IndexError
            if (
                type(board[self.y + 1][self.x - 1]) == White
                and board[self.y + 2][self.x - 2] == None
            ):
                valid_moves.append(
                    {
                        "coords": (self.x - 2, self.y + 2),
                        "cap_piece": board[self.y + 1][self.x - 1],
                    }
                )
        except IndexError:
            pass
        return valid_moves

    def draw(self):
        WIN.blit(BLACK_PIECE_IMG, board_to_coords(self.x, self.y))


class Clear(Piece):
    instances = []

    def __init__(self, x, y, root_piece):
        super().__init__(x, y)
        self.__class__.instances.append(self)
        self.cap_piece = None
        self.root_piece = root_piece

    def set_cap_piece(self, cap_piece):
        self.cap_piece = cap_piece


class Clear_White(Clear):
    def draw(self):
        WIN.blit(CLEAR_WHITE_PIECE_IMG, board_to_coords(self.x, self.y))


class Clear_Black(Clear):
    def draw(self):
        WIN.blit(CLEAR_BLACK_PIECE_IMG, board_to_coords(self.x, self.y))
