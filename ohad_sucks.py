import pygame
import os
from checkers_classes import (
    Clear,
    Clear_White,
    Clear_Black,
    White,
    Black,
    White_Pawn,
    Black_Pawn,
    White_King,
    Black_King,
    board,
    WIN,
    TILE_SIZE,
    WIN_SIZE,
)

pygame.mixer.init()
pygame.font.init()

WIN_FONT = pygame.font.Font(os.path.join("Assets", "Calibri.ttf"), 120)

PIECE_STEP_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Piece_step.wav"))
CAPTURE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Capture.wav"))


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


def win(is_white):
    if is_white:
        win_text = WIN_FONT.render("White Wins!", 1, "white")
    else:
        win_text = WIN_FONT.render("Black Wins!", 1, "white")
    WIN.blit(
        win_text,
        (
            WIN_SIZE[0] // 2 - win_text.get_width() // 2,
            WIN_SIZE[1] // 2 - win_text.get_height(),
        ),
    )
    pygame.display.update()
    pygame.time.wait(3000)


def starting_position():
    global board
    # Breaks everything for some reason
    # ! board = [[None for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            if (i % 2 + j % 2) % 2 == 1:
                if i <= 2:
                    board[i][j] = Black_Pawn(j, i)
                if i >= 5:
                    board[i][j] = White_Pawn(j, i)


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
                            if White.instances == [] or Black.instances == []:
                                win(white_turn)
                            Clear.instances.clear()
                            valid_moves = piece.root_piece.second_cap()
                            if valid_moves != []:
                                capturer = piece.root_piece
                                multi_capture = True
                                break
                        if (
                            type(piece.root_piece) == White_Pawn
                            and piece.root_piece.y == 0
                        ):
                            board[piece.root_piece.y][piece.root_piece.x] = White_King(
                                piece.root_piece.x, piece.root_piece.y
                            )
                            White.instances.remove(piece.root_piece)
                        if (
                            type(piece.root_piece) == Black_Pawn
                            and piece.root_piece.y == 7
                        ):
                            board[piece.root_piece.y][piece.root_piece.x] = Black_King(
                                piece.root_piece.x, piece.root_piece.y
                            )
                            Black.instances.remove(piece.root_piece)

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
