from .hex import Hex
from .piece import Piece


class Board:
    def __init__(
        self,
        difficulty: int,
        selected_piece: Hex = Hex(0, 0),
    ):
        self.board = []
        self.selected_piece = selected_piece
        self.black_pieces_placed = 0
        self.white_pieces_placed = 0
        self.difficulty = difficulty

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

    def remove_piece_by_hex(self, hex: Hex) -> Piece | None:
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
        raise ValueError("Element doesn't exist in remove_piece_by_hex function")

    def select_piece_by_hex(self, hex: Hex) -> Piece | None:
        for piece in self.board:
            if piece.hex.q == hex.q and piece.hex.r == hex.r and piece.hex.s == hex.s:
                return piece
        # raise ValueError("Element doesn't exist in select_piece_by_hex function")

    def is_valid_move(self, piece: Piece, to_hex: Hex) -> bool:
        # game-specific logic here
        # let's assume any empty hex is a valid move temp
        return self.select_piece_by_hex(to_hex) is None

    def move(self, from_hex: Hex, to_hex: Hex):
        piece = self.select_piece_by_hex(from_hex)
        if piece:
            if self.is_valid_move(piece, to_hex):
                piece.hex = to_hex
            else:
                print("Invalid move")
        else:
            print("Piece not found at the given hex")
