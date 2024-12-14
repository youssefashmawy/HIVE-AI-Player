from .hex import Hex
from abc import abstractmethod
from hive.constants import Consts
from pygame.surface import Surface
from typing import Literal

class Piece:
    def __init__(self, piece_name: Literal["Queen","Ant","Hopper","Spider","Beetle"], piece_type: Literal["black","white"]):
        assert piece_type.lower() in ["black", "white"]
        self.piece_name: Literal["Queen","Ant","Hopper","Spider","Beetle"] = piece_name.capitalize()
        self.piece_type: Literal["black","white"] = piece_type.lower()

    def __repr__(self) -> str:
        return f"{self.piece_type.capitalize()} {self.piece_name.capitalize()}"

    def __eq__(self, other: "Piece"):
        return (self.piece_name) == (other.piece_name) and (self.piece_type) == (
            other.piece_type
        )

    def get_image(self) -> Surface:
        return ""

    @abstractmethod
    def get_legal_moves(self, hex: Hex, board: list[list["Piece"]]) -> list[Hex]:
        """
        Abstract method to calculate legal moves.

        Args:
            board (List[List[Piece]]): A list of stacks (each stack is a list of Pieces).

        Returns:
            List[Hex]: A list of legal moves represented by Pieces.
        """
        pass


# Define specific piece classes
class Queen(Piece):
    def __init__(self, piece_type):
        """
        Initialize the Queen piece.
        """
        super().__init__(piece_name="Queen", piece_type=piece_type)

    def get_image(self) -> Surface:
        return Consts.white_queen if self.piece_type == "white" else Consts.black_queen


class Spider(Piece):
    def __init__(self, piece_type):
        """
        Initialize the Spider piece.
        """
        super().__init__(piece_name="Spider", piece_type=piece_type)

    def get_image(self) -> Surface:
        return (
            Consts.white_spider if self.piece_type == "white" else Consts.black_spider
        )


class Ant(Piece):
    def __init__(self, piece_type):
        """
        Initialize the Ant piece.
        """
        super().__init__(piece_name="Ant", piece_type=piece_type)

    def get_image(self) -> Surface:
        return Consts.white_ant if self.piece_type == "white" else Consts.black_ant


class Hopper(Piece):
    def __init__(self, piece_type):
        """
        Initialize the Hopper piece.
        """
        super().__init__(piece_name="Hopper", piece_type=piece_type)

    def get_image(self) -> Surface:
        return (
            Consts.white_grasshopper
            if self.piece_type == "white"
            else Consts.black_grasshopper
        )


class Beetle(Piece):
    def __init__(self, piece_type):
        """
        Initialize the Beetle piece.
        """
        super().__init__(piece_name="Beetle", piece_type=piece_type)

    def get_image(self) -> Surface:
        return (
            Consts.white_beetle if self.piece_type == "white" else Consts.black_beetle
        )
