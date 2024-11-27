from .hex import Hex
from abc import abstractmethod


class Piece(Hex):
    def __init__(self, hex: Hex, piece_name: str, piece_type: str):
        self.hex = hex
        assert piece_type.lower() in ["black", "white"]
        self.piece_name = piece_name.lower()
        self.piece_type = piece_type.lower()

    def __repr__(self) -> str:
        return f"{self.piece_type.capitalize()} {self.piece_name.capitalize()} at {self.hex}"

    @abstractmethod
    def get_legal_moves() -> list[Hex]:
        pass
