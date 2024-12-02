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

    def get_legal_moves_piece(self, board: list[list["Piece"]]) -> list["Hex"]:
        """
        Calculate valid moves for a Grasshopper in the Hive game.

        Rules for Grasshopper movement:

        The Grasshopper does not move around the outside of the Hive like the other creatures. Instead, it jumps from its space over any number of pieces (but at least one) to the next unoccupied space along a straight row of joined pieces.

        """

        legal_moves = []

        # get all ocuppied places on board
        occupied_places = {piece.hex for stack in board for piece in stack if piece}

        for m in MOVES:

            current_hex = Hex(self.hex.q + m.q, self.hex.r + m.r)

            jumped_over = 0

            # jump till find a sitable place
            while current_hex in occupied_places:
                jumped_over += 1
                current_hex = Hex(current_hex.q + m.q, current_hex.r + m.r)

            # Valid move if jumped at least one piece and landed on empty hex
            if jumped_over > 0 and current_hex not in occupied_places:
                legal_moves.append(current_hex)

        return legal_moves

    def move(self, destination: Hex):

        self.hex = destination
        self.is_placed = True
