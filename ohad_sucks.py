import pygame
import os
from checkers_classes import (
    Clear,
    Pawn,
    King,
    Empty,
    board,
    pawn_king_instances,
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
                    board[i][j] = Pawn(j, i, "black")
                if i >= 5:
                    board[i][j] = Pawn(j, i, "white")


def main():
    clock = pygame.time.Clock()
    run = True
    white_turn = True
    multi_capture = False
    pawn: Pawn
    king: King
    clear: Clear
    colors = {True: "white", False: "black"}
    starting_position()
    while run:
        WIN.fill("black")
        draw_board()
        for piece in pawn_king_instances["white"] + pawn_king_instances["black"]:
            piece.draw()
        for clear in Clear.clear_instances["white"] + Clear.clear_instances["black"]:
            clear.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for clear in (
                    Clear.clear_instances["white"] + Clear.clear_instances["black"]
                ):
                    if clear.collide():
                        PIECE_STEP_SOUND.play()
                        clear.root_piece.set_pos(clear.x, clear.y)
                        if clear.cap_piece != None:
                            board[clear.cap_piece.y][clear.cap_piece.x] = Empty()
                            pawn_king_instances[colors[not white_turn]].remove(
                                clear.cap_piece
                            )
                            CAPTURE_SOUND.play()
                            if (
                                pawn_king_instances["white"] == []
                                or pawn_king_instances["black"] == []
                            ):
                                win(white_turn)
                            Clear.clear_instances["white"].clear()
                            Clear.clear_instances["black"].clear()
                            valid_moves = clear.root_piece.second_cap()
                            if valid_moves != []:
                                capturer = clear.root_piece
                                multi_capture = True
                                break
                        white_turn = not white_turn
                        if (
                            type(clear.root_piece) == Pawn
                            and clear.root_piece.y == clear.root_piece.crown_row
                        ):
                            board[clear.root_piece.y][clear.root_piece.x] = King(
                                clear.root_piece.x,
                                clear.root_piece.y,
                                clear.root_piece.color,
                            )
                            pawn_king_instances[clear.root_piece.color].remove(
                                clear.root_piece
                            )
                        multi_capture = False
                        break
                if not multi_capture:
                    for piece in pawn_king_instances[colors[white_turn]]:
                        if piece.collide():
                            Clear.clear_instances["white"].clear()
                            Clear.clear_instances["black"].clear()
                            valid_moves = piece.find_valid()
                            for i in valid_moves:
                                Clear(
                                    i["coords"][0],
                                    i["coords"][1],
                                    colors[white_turn],
                                    piece,
                                )
                                if "cap_piece" in i:
                                    Clear.clear_instances[colors[white_turn]][
                                        -1
                                    ].set_cap_piece(i["cap_piece"])
                            break
                        else:
                            Clear.clear_instances["white"].clear()
                            Clear.clear_instances["black"].clear()
                else:
                    for i in valid_moves:
                        Clear(
                            i["coords"][0],
                            i["coords"][1],
                            colors[white_turn],
                            capturer,
                        )
                        Clear.clear_instances[colors[white_turn]][-1].set_cap_piece(
                            i["cap_piece"]
                        )
        clock.tick(30)
        pygame.display.update()


if __name__ == "__main__":
    main()
