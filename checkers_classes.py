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


def board_to_coords(x: int, y: int):
    # Convert coordinates on the board to coordinates of the display (e.g. 2, 3 to 200, 400)
    ratio = WIN_SIZE[0] / 8
    x = x * ratio
    y = y * ratio
    return x, y


class Empty:
    def __init__(self):
        self.color = None


board = [[Empty() for _ in range(8)] for _ in range(8)]
pawn_king_instances = {"white": [], "black": []}


class Piece:
    all_instances = {"white": [], "black": []}

    def __init__(self, x: int, y: int, color: str):
        self.x = x
        self.y = y
        self.color = color
        if color == "white":
            self.__class__.all_instances["white"].append(self)
        elif color == "black":
            self.__class__.all_instances["black"].append(self)
        self.rect = pygame.Rect((board_to_coords(self.x, self.y), (TILE_SIZE)))

    def set_pos(self, x, y):
        board[self.y][self.x] = Empty()
        self.x = x
        self.y = y
        board[self.y][self.x] = self
        self.rect.topleft = board_to_coords(x, y)

    def second_cap(self) -> list:
        valid_moves = []
        if self.y > 1:
            if self.x > 1:
                if (
                    board[self.y - 1][self.x - 1].color == self.opp_color
                    and board[self.y - 2][self.x - 2].color == None
                ):
                    valid_moves.append(
                        {
                            "coords": (self.x - 2, self.y - 2),
                            "cap_piece": board[self.y - 1][self.x - 1],
                        }
                    )
            if self.x < 6:
                if (
                    board[self.y - 1][self.x + 1].color == self.opp_color
                    and board[self.y - 2][self.x + 2].color == None
                ):
                    valid_moves.append(
                        {
                            "coords": (self.x + 2, self.y - 2),
                            "cap_piece": board[self.y - 1][self.x + 1],
                        }
                    )
        if self.y < 6:
            if self.x > 1:
                if (
                    board[self.y + 1][self.x - 1].color == self.opp_color
                    and board[self.y + 2][self.x - 2].color == None
                ):
                    valid_moves.append(
                        {
                            "coords": (self.x - 2, self.y + 2),
                            "cap_piece": board[self.y + 1][self.x - 1],
                        }
                    )
            if self.x < 6:
                if (
                    board[self.y + 1][self.x + 1].color == self.opp_color
                    and board[self.y + 2][self.x + 2].color == None
                ):
                    valid_moves.append(
                        {
                            "coords": (self.x - 2, self.y + 2),
                            "cap_piece": board[self.y + 1][self.x + 1],
                        }
                    )
        return valid_moves

    def collide(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def draw(self):
        WIN.blit(self.img, board_to_coords(self.x, self.y))


class Pawn(Piece):
    pawn_instances = {"white": [], "black": []}

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if color == "white":
            self.img = WHITE_PAWN_IMG
            self.opp_color = "black"
            self.direction = -1
            self.crown_row = 0
            self.__class__.pawn_instances["white"].append(self)
            pawn_king_instances["white"].append(self)
        elif color == "black":
            self.img = BLACK_PAWN_IMG
            self.opp_color = "white"
            self.direction = 1
            self.crown_row = 7
            self.__class__.pawn_instances["black"].append(self)
            pawn_king_instances["black"].append(self)

    def find_valid(self) -> list:
        valid_moves = []
        if self.x > 0:
            if board[self.y + self.direction][self.x - 1].color == None:
                valid_moves.append({"coords": (self.x - 1, self.y + self.direction)})
            elif self.x > 1 and abs(self.crown_row - self.y) > 1:
                if (
                    board[self.y + self.direction][self.x - 1].color == self.opp_color
                    and board[self.y + self.direction * 2][self.x - 2].color == None
                ):
                    valid_moves.append(
                        {
                            "coords": (self.x - 2, self.y + self.direction * 2),
                            "cap_piece": board[self.y + self.direction][self.x - 1],
                        }
                    )
        if self.x < 7:
            if board[self.y + self.direction][self.x + 1].color == None:
                valid_moves.append({"coords": (self.x + 1, self.y + self.direction)})
            elif self.x < 6 and abs(self.crown_row - self.y) > 1:
                if (
                    board[self.y + self.direction][self.x + 1].color == self.opp_color
                    and board[self.y + self.direction * 2][self.x + 2].color == None
                ):
                    valid_moves.append(
                        {
                            "coords": (self.x + 2, self.y + self.direction * 2),
                            "cap_piece": board[self.y + self.direction][self.x + 1],
                        }
                    )
        return valid_moves


class King(Piece):
    king_instances = {"white": [], "black": []}

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if color == "white":
            self.img = WHITE_KING_IMG
            self.__class__.king_instances["white"].append(self)
            pawn_king_instances["white"].append(self)
        elif color == "black":
            self.img = BLACK_KING_IMG
            self.__class__.king_instances["black"].append(self)
            pawn_king_instances["black"].append(self)

    def find_valid(self):
        valid_moves = []
        for i in range(min(self.x, self.y)):
            if board[self.y - i - 1][self.x - i - 1] == self.color:
                break
            elif board[self.y - i - 1][self.x - i - 1] == self.opp_color:
                if board[self.y - i - 2][self.x - i - 2].color == None:
                    valid_moves.append(
                        {
                            "coords": (self.x - i - 2, self.y - i - 2),
                            "cap_piece": board[self.y - i - 1][self.x - i - 1],
                        }
                    )
                break
            valid_moves.append(
                {
                    "coords": (self.x - i - 1, self.y - i - 1),
                }
            )
        for i in range(min(7 - self.x, self.y)):
            if board[self.y - i - 1][self.x + i + 1] == self.color:
                break
            elif board[self.y - i - 1][self.x + i + 1] == self.opp_color:
                if board[self.y - i - 2][self.x + i + 2].color == None:
                    valid_moves.append(
                        {
                            "coords": (self.x + i + 2, self.y - i - 2),
                            "cap_piece": board[self.y - i - 1][self.x + i + 1],
                        }
                    )
                break
            valid_moves.append(
                {
                    "coords": (self.x + i + 1, self.y - i - 1),
                }
            )
        for i in range(min(self.x, 7 - self.y)):
            if board[self.y + i + 1][self.x - i - 1] == self.color:
                break
            elif board[self.y + i + 1][self.x - i - 1] == self.opp_color:
                if board[self.y + i + 2][self.x - i - 2].color == None:
                    valid_moves.append(
                        {
                            "coords": (self.x - i - 2, self.y + i + 2),
                            "cap_piece": board[self.y + i + 1][self.x - i - 1],
                        }
                    )
                break
            valid_moves.append(
                {
                    "coords": (self.x - i - 1, self.y + i + 1),
                }
            )
        for i in range(min(7 - self.x, 7 - self.y)):
            if board[self.y + i + 1][self.x + i + 1] == self.color:
                break
            elif board[self.y + i + 1][self.x + i + 1] == self.opp_color:
                if board[self.y + i + 2][self.x + i + 2].color == None:
                    valid_moves.append(
                        {
                            "coords": (self.x + i + 2, self.y + i + 2),
                            "cap_piece": board[self.y + i + 1][self.x + i + 1],
                        }
                    )
                break
            valid_moves.append(
                {
                    "coords": (self.x + i + 1, self.y + i + 1),
                }
            )
        return valid_moves


class Clear(Piece):
    clear_instances = {"white": [], "black": []}

    def __init__(self, x, y, color, root_piece):
        super().__init__(x, y, color)
        if self.color == "white":
            self.__class__.clear_instances["white"].append(self)
            self.img = CLEAR_WHITE_PAWN_IMG
        elif self.color == "black":
            self.__class__.clear_instances["black"].append(self)
            self.img = CLEAR_BLACK_PAWN_IMG
        self.root_piece = root_piece
        self.cap_piece = None

    def set_cap_piece(self, cap_piece):
        self.cap_piece = cap_piece
