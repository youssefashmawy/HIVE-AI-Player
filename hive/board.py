from .hex import Hex
from .piece import Piece


class Board:
    def __init__(
        self,
        selected_piece: Hex = Hex(0, 0),
    ):
        self.board = []
        self.selected_piece = selected_piece
        self.black_pieces_placed = 0
        self.white_pieces_placed = 0

    def set_selected_piece(self, selected_piece: Hex):
        self.selected_piece = selected_piece

    def increment_pieces_placed(self, piece: Piece):

        self.board.insert(0, piece)

        if piece.piece_type == "black":
            self.black_pieces_placed += 1
        elif piece.piece_type == "white":
            self.white_pieces_placed += 1

    def __repr__(self):
        return f"Board = {self.board}"

    def remove_piece(self, hex: Hex) -> Piece | None:
        """removes a piece from the board and returns it

        Args:
            hex (Hex): Pressed element required to be moved

        Returns:
            Piece: The element in the board required to be removed
        """
        for piece in self.board:
            if piece.hex.q == hex.q and piece.hex.r == hex.r and piece.hex.s == hex.s:
                self.board.remove(piece)
                return piece
        print("Element doesn't exist")
        return None

    def move(self, hex: Hex): ...
