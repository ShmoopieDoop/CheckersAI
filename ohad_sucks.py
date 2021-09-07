import pygame
import os
from checkers_classes import (
    Clear,
    Clear_White,
    Clear_Black,
    White,
    Black,
    board,
    WIN,
    TILE_SIZE,
)

pygame.mixer.init()

PIECE_STEP_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Piece_step.wav"))
CAPTURE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Capture.wav"))

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


def draw_board():
    for i in range(8):
        for j in range(8):
            tile = pygame.Rect(
                i * TILE_SIZE[0],
                j * TILE_SIZE[1],
                TILE_SIZE[0],
                TILE_SIZE[1],
            )
            if i % 2 + j % 2 == 1:
                pygame.draw.rect(
                    WIN,
                    (0, 50, 100),
                    tile,
                )

            else:
                pygame.draw.rect(
                    WIN,
                    (255, 242, 212),
                    tile,
                )


def starting_position():
    global board
    for i in range(8):
        for j in range(8):
            if (i % 2 + j % 2) % 2 == 1:
                if i <= 2:
                    board[i][j] = Black(j, i)
                if i >= 5:
                    board[i][j] = White(j, i)


def main():
    clock = pygame.time.Clock()
    run = True
    white_turn = True
    multi_capture = False
    starting_position()
    while run:
        WIN.fill("black")
        draw_board()
        for piece in White.instances:
            piece.draw()
        for piece in Black.instances:
            piece.draw()
        for piece in Clear.instances:
            piece.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for piece in Clear.instances:
                    if piece.collide():
                        PIECE_STEP_SOUND.play()
                        piece.root_piece.set_pos(piece.x, piece.y)
                        if piece.cap_piece != None:
                            board[piece.cap_piece.y][piece.cap_piece.x] = None
                            try:
                                White.instances.remove(piece.cap_piece)
                            except ValueError:
                                pass
                            try:
                                Black.instances.remove(piece.cap_piece)
                            except ValueError:
                                pass
                            CAPTURE_SOUND.play()
                            Clear.instances.clear()
                            valid_moves = piece.root_piece.second_cap()
                            if valid_moves != []:
                                capturer = piece.root_piece
                                multi_capture = True
                                break
                        white_turn = not white_turn
                        multi_capture = False
                if white_turn:
                    if not multi_capture:
                        for piece in White.instances:
                            if piece.collide():
                                Clear.instances.clear()
                                valid_moves = piece.find_valid()
                                for i in valid_moves:
                                    Clear_White(i["coords"][0], i["coords"][1], piece)
                                    if "cap_piece" in i:
                                        Clear.instances[-1].set_cap_piece(
                                            i["cap_piece"]
                                        )
                                break
                            else:
                                Clear.instances.clear()
                    else:
                        for i in valid_moves:
                            Clear_White(i["coords"][0], i["coords"][1], capturer)
                            Clear.instances[-1].set_cap_piece(i["cap_piece"])
                else:
                    if not multi_capture:
                        for piece in Black.instances:
                            if piece.collide():
                                Clear.instances.clear()
                                valid_moves = piece.find_valid()
                                for i in valid_moves:
                                    Clear_Black(i["coords"][0], i["coords"][1], piece)
                                    if "cap_piece" in i:
                                        Clear.instances[-1].set_cap_piece(
                                            i["cap_piece"]
                                        )
                                break
                            else:
                                Clear.instances.clear()
                    else:
                        for i in valid_moves:
                            Clear_Black(i["coords"][0], i["coords"][1], capturer)
                            Clear.instances[-1].set_cap_piece(i["cap_piece"])
        clock.tick(30)
        pygame.display.update()


if __name__ == "__main__":
    main()
