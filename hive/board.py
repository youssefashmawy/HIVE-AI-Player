from .hex import Hex


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

    def increment_pieces_placed(self, hex: Hex, piece_name: str, piece_type: str):

        self.board.insert(
            0,
            [
                piece_name.lower(),
                piece_type.lower(),
                hex.q,
                hex.r,
                hex.s,
            ],
        )
        if piece_type.lower() == "black":
            self.black_pieces_placed += 1
        elif piece_type.lower() == "white":
            self.white_pieces_placed += 1

    def __repr__(self):
        return f"Board = {self.board}"

    def remove_piece(self, hex: Hex) -> list[str, str, int, int, int]:
        """removes a piece from the board and returns it

        Args:
            hex (Hex): Pressed element required to be moved

        Returns:
            list[str,str,int,int,int]: The element in the board required to be removed with the following values piece_name, piece_type(black or white), q, r, s
        """
        for piece in self.board:
            if piece[2] == hex.q and piece[3] == hex.r and piece[4] == hex.s:
                self.board.remove(piece)
                return piece
        print("Element doesn't exist")
        return None

    def move(self, hex: Hex): ...
