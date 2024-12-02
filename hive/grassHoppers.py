from .board import Board
from .hex import Hex
from .piece import Piece


MOVES = [
    Hex(0, -1),  # North
    Hex(1, -1),  # Northeast
    Hex(1, 0),  # East
    Hex(0, 1),  # South
    Hex(-1, 1),  # Southwest
    Hex(-1, 0),  # West
]  # grassHopper must move in straight line


class GrassHopper(Piece):
    count = 3

    def __init__(self, hex: Hex, piece_type: str, difficulty: int):
        super().__init__(hex, "grasshopper", piece_type)
        self.difficulty = difficulty

    def get_legal_moves_piece(self, board: list[list[Piece]]) -> list[Hex]:
        """
        Calculate valid moves for a Grasshopper in the Hive game.

        Rules for Grasshopper movement:
        1. Can only move in a straight line (like a rook in chess)
        2. Must jump over at least one piece
        3. Land on the first empty space after jumping
        4. Cannot jump over empty spaces
        """

        legal_moves = []
