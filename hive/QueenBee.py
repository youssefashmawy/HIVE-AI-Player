from .piece import Piece
from .board import Board
from .hex import Hex
class QueenBee(Piece):
    count = 1
    def __init__(self, hex: Hex, piece_name: str, piece_type: str, difficulty: int):
        super().__init__(hex, piece_name, piece_type)
        self.difficulty = difficulty

    def __repr__(self):
        return f"QueenBee {self.piece_name.capitalize()} at {self.hex} with difficulty {self.difficulty}"

    def get_legal_moves_piece(self, board: Board) -> list[Hex]:

        legal_moves = []
        neighbors=self.get_neighbors(hex,board)
        for neighbor in neighbors:
            if self.surrounded_neighbors(neighbor,board):
                 legal_moves.append(neighbor)
                    
        return legal_moves    
                
                
    def get_neighbors(hex: Hex, board: Board) -> list[Hex]:

  
     directions = [
        (1, 0),   # Right
        (1, -1),  # Top-right
        (0, -1),  # Top-left
        (-1, 0),  # Left
        (-1, 1),  # Bottom-left
        (0, 1)    # Bottom-right
      ]
    
     neighbors = []

     for direction in directions:
           neighbor_hex = Hex(hex.q + direction[0], hex.r + direction[1], hex.s + (-direction[0] - direction[1]))
        
        
     if not any(piece.hex.q == neighbor_hex.q and piece.hex.r == neighbor_hex.r and piece.hex.s == neighbor_hex.s for piece in board.board):
            neighbors.append(neighbor_hex)
     return neighbors
    
    def surrounded_neighbors(hex:Hex, board:Board)->bool:
     directions = [
        (1, 0),   # Right
        (1, -1),  # Top-right
        (0, -1),  # Top-left
        (-1, 0),  # Left
        (-1, 1),  # Bottom-left
        (0, 1)    # Bottom-right
      ]
     for direction in directions:
          neighbor_hex = Hex(hex.q + direction[0], hex.r + direction[1], hex.s + (-direction[0] - direction[1]))
          if any(piece.hex.q == neighbor_hex.q and piece.hex.r == neighbor_hex.r and piece.hex.s == neighbor_hex.s for piece in board.board):
            return True
        
     return False
        
    
    
     
        
        
                
        
            
            
            
            
        
        
        
        
