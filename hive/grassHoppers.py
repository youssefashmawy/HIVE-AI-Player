from .board import Board
from .hex import Hex
from .piece import Piece

# (q,r)
ITERATIVE_MOVES = {[0, 1], [0, -1], [1, 0], [-1, 0]}


class GrassHopper(Piece):
    count = 3

    def __init__(self, difficulty: int):
        self.difficulty = difficulty
