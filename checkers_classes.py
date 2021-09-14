import pygame
import os

WIN_SIZE = 800, 800
WIN = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("Checkers")

TILE_SIZE = WIN_SIZE[0] / 8, WIN_SIZE[1] / 8

WHITE_PAWN_IMG = pygame.image.load(os.path.join("Assets", "white_piece.png")).convert()
WHITE_PAWN_IMG.set_colorkey("white")
BLACK_PAWN_IMG = pygame.image.load(os.path.join("Assets", "black_piece.png")).convert()
BLACK_PAWN_IMG.set_colorkey("white")
CLEAR_WHITE_PAWN_IMG = pygame.image.load(
    os.path.join("Assets", "clear_white_piece.png")
).convert_alpha()
CLEAR_WHITE_PAWN_IMG.set_colorkey("white")
CLEAR_BLACK_PAWN_IMG = pygame.image.load(
    os.path.join("Assets", "clear_black_piece.png")
).convert_alpha()
CLEAR_BLACK_PAWN_IMG.set_colorkey("white")
WHITE_KING_IMG = pygame.image.load(os.path.join("Assets", "white_king.png")).convert()
WHITE_KING_IMG.set_colorkey("white")
BLACK_KING_IMG = pygame.image.load(os.path.join("Assets", "black_king.png")).convert()
BLACK_KING_IMG.set_colorkey("white")
CLEAR_WHITE_KING_IMG = pygame.image.load(
    os.path.join("Assets", "clear_white_king.png")
).convert_alpha()
CLEAR_WHITE_KING_IMG.set_colorkey("white")
CLEAR_BLACK_KING_IMG = pygame.image.load(
    os.path.join("Assets", "clear_black_king.png")
).convert_alpha()
CLEAR_BLACK_KING_IMG.set_colorkey("white")

board = [[None for _ in range(8)] for _ in range(8)]


def board_to_coords(x: int, y: int):
    # Convert coordinates on the board to coordinates of the display (e.g. 2, 3 to 200, 400)
    ratio = WIN_SIZE[0] / 8
    x = x * ratio
    y = y * ratio
    return x, y


class Piece:
    instances = {"white": [], "black": []}

    def __init__(self, x: int, y: int, color: str):
        self.x = x
        self.y = y
        self.color = color
        if color == "white":
            self.__class__.instances["white"].append(self)
        elif color == "black":
            self.__class__.instances["black"].append(self)
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


class Pawn(Piece):
    instances = {"white": [], "black": []}

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if color == "white":
            self.img = WHITE_PAWN_IMG
            self.opp_color = "black"
            self.__class__.instances["white"].append(self)
        elif color == "black":
            self.img = BLACK_PAWN_IMG
            self.opp_color = "white"
            self.__class__.instances["black"].append(self)

    def find_valid(self) -> list:
        valid_moves = []
        direction = -1
        crown_row = 0
        if self.color == "black":
            direction = 1
            crown_row = 7
        if self.x > 0:
            if board[self.y + direction][self.x - 1] == None:
                valid_moves.append({"coords": (self.x - 1, self.y + direction)})
            elif self.x > 1 and abs(crown_row - self.y) > 1:
                if (
                    board[self.y + direction][self.x - 1].color == self.opp_color
                    and board[self.y + direction * 2][self.x - 2] == None
                ):
                    valid_moves.append({"coords": (self.x - 2, self.y + direction * 2)})
        if self.x < 7:
            if board[self.y + direction][self.x + 1] == None:
                valid_moves.append({"coords": (self.x + 1, self.y + direction)})
            elif self.x < 6 and abs(crown_row - self.y) > 1:
                if (
                    board[self.y + direction][self.x + 1].color == self.opp_color
                    and board[self.y + direction * 2][self.x + 2] == None
                ):
                    valid_moves.append({"coords": (self.x + 2, self.y + direction * 2)})
        return valid_moves

    def second_cap(self) -> list:
        valid_moves = []
        if self.y > 1:
            if self.x > 1:
                if (
                    board[self.y - 1][self.x - 1].color == self.opp_color
                    and board[self.y - 1 * 2][self.x - 2] == None
                ):
                    valid_moves.append({"coords": (self.x - 2, self.y - 1 * 2)})
            if self.x < 6:
                if (
                    board[self.y - 1][self.x + 1].color == self.opp_color
                    and board[self.y - 1 * 2][self.x - 2] == None
                ):
                    valid_moves.append({"coords": (self.x - 2, self.y - 1 * 2)})
        if self.y < 6:
            if self.x > 1:
                if (
                    board[self.y + 1][self.x - 1].color == self.opp_color
                    and board[self.y + 1 * 2][self.x - 2] == None
                ):
                    valid_moves.append({"coords": (self.x - 2, self.y + 1 * 2)})
            if self.x < 6:
                if (
                    board[self.y + 1][self.x + 1].color == self.opp_color
                    and board[self.y + 1 * 2][self.x - 2] == None
                ):
                    valid_moves.append({"coords": (self.x - 2, self.y + 1 * 2)})
        return valid_moves

    def draw(self):
        WIN.blit(self.img, board_to_coords(self.x, self.y))


class King(Piece):
    instances = {"white": [], "black": []}

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if color == "white":
            self.__class__.instances["white"].append(self)
            self.img = WHITE_KING_IMG
        elif color == "black":
            self.__class__.instances["black"].append(self)
            self.img = BLACK_KING_IMG

    def draw(self):
        WIN.blit(self.img, board_to_coords(self.x, self.y))


class Clear(Piece):
    instances = {"white": [], "black": []}

    def __init__(self, x, y, color, root_piece):
        super().__init__(x, y, color)
        if self.color == "white":
            self.__class__.instances["white"].append(self)
            self.img = CLEAR_WHITE_PAWN_IMG
        elif self.color == "black":
            self.__class__.instances["black"].append(self)
            self.img = CLEAR_BLACK_PAWN_IMG
        self.root_piece = root_piece
        self.cap_piece = None

    def set_cap_piece(self, cap_piece):
        self.cap_piece = cap_piece

    def draw(self):
        WIN.blit(self.img, board_to_coords(self.x, self.y))
