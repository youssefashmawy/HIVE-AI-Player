from .piece import Piece
from .board import Board
from .hex import Hex
class Spider(Piece):
    count = 2

    def __init__(self, hex: Hex, piece_name: str, piece_type: str, difficulty: int):
        super().__init__(hex, piece_name, piece_type)
        self.difficulty = difficulty

    def __repr__(self):
        return f"Spider {self.piece_name.capitalize()} at {self.hex} with difficulty {self.difficulty}"

    def get_legal_moves_piece(self, board: Board) -> list[Piece]:

        legal_moves = []
        directions = self.get_directions() 
        
        # Spider moves 3 spaces in a straight line, so we check 3 times in each direction
        for direction in directions:
            temp_hex = self.hex
            valid_move = True
            # Try to move 3 steps in the chosen direction
            for _ in range(3):
                temp_hex = self.add_direction(temp_hex, direction)  # Get the new hex after move
                
                # Check if the new hex is valid (e.g., no occupied space or out of bounds)
                if not board.is_valid_move(self, temp_hex):
                    valid_move = False
                    break
            
            # If the move is valid, add it to the legal moves list
            if valid_move:
                legal_moves.append(Piece(temp_hex, self.piece_name, self.piece_type))
        
        return legal_moves

    def get_directions(self) -> list[tuple[int, int]]:
        """
        This method returns the 6 possible movement directions on a hexagonal grid.
        These directions are typically represented as (q, r) axial coordinates in the hexagonal grid.
        """
        return [
            (1, 0),  # Right
            (1, -1),  # Top-Right
            (0, -1),  # Top
            (-1, 0),  # Left
            (-1, 1),  # Bottom-Left
            (0, 1)  # Bottom
        ]
    
    def add_direction(self, hex: Hex, direction: tuple[int, int]) -> Hex:
        """
        Adds a direction to a given hex, which effectively moves the piece to the next hex in the grid.
        """
        return Hex(hex.q + direction[0], hex.r + direction[1])