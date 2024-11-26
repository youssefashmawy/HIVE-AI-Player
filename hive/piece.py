from .hex import Hex


class Piece(Hex):
    def __init__(self, hex, piece_name: str, piece_type: str):
        self.hex = hex
        assert piece_type.lower() == "black" or piece_type.lower() == "white"
        self.piece_name = piece_name.lower()
        self.piece_type = piece_type.lower()

    def __repr__(self) -> str:
        return (
            f"Name: {self.piece_name}" + f"Type:{self.piece_type}" + super().__repr__()
        )
