from .hex import Hex
from abc import abstractmethod


class Piece(Hex):
    def __init__(self, hex: Hex, piece_name: str, piece_type: str, count: int = 1):
        self.hex = hex
        assert piece_type.lower() in ["black", "white"]
        self.piece_name = piece_name.lower()
        self.piece_type = piece_type.lower()
        # To check if this piece in the game array or not
        self.is_placed = False

    def __repr__(self) -> str:
        return f"{self.piece_type.capitalize()} {self.piece_name.capitalize()} at {self.hex} was placed:{self.is_placed}"

    def __eq__(self, other: "Piece"):
        return (self.hex) == (other.hex)

    def generate_adj_hexs(self) -> dict["Hex"]:
        directions = {
            "North": Hex(self.hex.q, self.hex.r - 1),
            "North_east": Hex(self.hex.q + 1, self.hex.r - 1),
            "South_east": Hex(self.hex.q + 1, self.hex.r),
            "South": Hex(self.hex.q, self.hex.r + 1),
            "South_west": Hex(self.hex.q - 1, self.hex.r + 1),
            "North_west": Hex(self.hex.q - 1, self.hex.r),
        }
        return directions

    def __hash__(self):
        return hash(self.hex)

    @abstractmethod
    def get_legal_moves() -> list["Piece"]:
        pass
