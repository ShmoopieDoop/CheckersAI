from checkers_classes import *
from math import inf
from copy import deepcopy


def get_possible_moves(board, is_white, is_multicapture) -> list[dict]:
    moves: list[dict] = []
    piece: Pawn or King
    if is_white:
        for piece in pawn_king_instances["white"]:
            moves.append({"piece": piece, "moves": piece.find_valid()})
    else:
        for piece in pawn_king_instances["black"]:
            moves.append({"piece": piece, "moves": piece.find_valid()})
    return moves


def evaluate_position(board: list[list]) -> int:
    return len(pawn_king_instances["white"]) - len(pawn_king_instances["black"])


def minimax(board: list[list], depth: int, is_white: bool):
    game_over = (
        True
        if pawn_king_instances["white"] == 0 or pawn_king_instances["black"] == 0
        else False
    )
    if depth == 0 or game_over:
        return evaluate_position(board)
    if is_white:
        val = -inf
        for move in get_possible_moves(board, True, False):
            pass
    else:
        pass