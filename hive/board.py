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
        self.black_pieces_moved = 0
        self.white_pieces_moved = 0
        self.unplaced_pieces = {}  # Unplaced pieces with counts
        self.difficulty = difficulty
        # To force first move in game to be in position 0,0,0
        self.is_first_move = True

    def set_selected_piece(self, selected_piece: Hex) -> None:
        self.selected_piece = selected_piece

    def increment_pieces_placed(self, piece: Piece) -> None:

        self.board.insert(0, piece)

    def __repr__(self):
        return f"Board = {self.board}\n\nboard = {self.board}, unplaced Pieces ={self.unplaced_pieces}"

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
        # not_break_hive and sliding and not_pinned
        return self.select_piece_by_hex(to_hex) is None

    def not_break_hive(self, piece: Piece) -> bool:
        # 1) Copy the game state without the piece you are inspecting
        copy_board = set(self.board)
        copy_board.discard(piece)  # Remove the piece from the copy

        # 2) Get the neighbors of this piece (before removing it of course)
        neighbours = self.get_neighbours(piece)
        if not neighbours:
            # If there are no neighbors(first move), removing this piece doesn't break the hive
            return True

        # 3) Conduct a breadth-first search from one of the neighbors
        queue = [neighbours[0]]
        visited = set()
        while queue:
            current_piece = queue.pop(0)
            if current_piece in visited:
                continue
            visited.add(current_piece)

            adj_hexes = current_piece.generate_adj_hexs().values()
            adj_pieces = [
                piece
                for piece in copy_board
                if piece.hex in adj_hexes and piece not in visited
            ]
            queue.extend(adj_pieces)

        # 4) Ensure all pieces in the copy_board are visited
        all_pieces_connected = visited == copy_board

        # 5) Check if all neighbors are in the visited nodes
        neighbors_in_visited = all(neighbor in visited for neighbor in neighbours)

        # Return True if no hive break occurs
        return all_pieces_connected and neighbors_in_visited

    def get_neighbours(self, piece: Piece) -> list[Piece]:
        """To get the neighbours of a piece

        Args:
            piece (Piece): The piece to get its neighbours

        Returns:
            list[Piece]: list of all the neighbours of our input piece
        """
        adj_hexes = piece.generate_adj_hexs().values()
        neighbours = []
        for piece in self.board:
            if piece.hex in adj_hexes:
                neighbours.append(piece)
        return neighbours

    def move(self, from_hex: Hex, to_hex: Hex):
        piece = self.select_piece_by_hex(from_hex)
        if piece:
            if self.is_valid_move(piece, to_hex):
                piece.hex = to_hex
                self.is_first_move = False
                if piece.is_placed == False:
                    self.board.append(piece)
                piece.is_placed = True

                if piece.piece_type == "black":
                    self.black_pieces_moved += 1
                elif piece.piece_type == "white":
                    self.white_pieces_moved += 1

            else:
                print("Invalid move")
        else:
            print("Piece not found at the given hex")

    def turn(self) -> bool:
        """Returns the turn of the current player

        Returns:
            bool: True -> white, False -> black
        """

        if self.board[0] == None or self.board[0].piece_type == "white":
            return True
        return False

    def total_moves(self) -> int:
        return self.black_pieces_moved + self.white_pieces_moved
