from .hex import Hex
from .piece import Piece
from collections import defaultdict
from typing import Union
from hive.piece import Ant, Hopper, Queen, Beetle, Spider
from collections import deque
from typing import Literal


class Board:
    def __init__(self, grid_radius: int = 5):

        self.board: dict[Hex, list[Piece]] = {}
        rsdiff = 1 * grid_radius
        # Create a hexagonal grid
        for q in range(-grid_radius, grid_radius + 1):
            for r in range(-grid_radius, grid_radius + 1):
                s = -q - r
                if abs(r - s) <= rsdiff:
                    # Add an empty stack at each hex coordinate
                    self.board[Hex(q, r)] = []

    def __repr__(self):
        return f"\n\nBoard = {self.board}\n\nboard = {self.board}, unplaced Pieces ={self.unplaced_pieces}"

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

    def hex_empty(self, hex: Hex):
        return hex not in self.board or not self.board[hex]

    def place_piece(self, target_hex: Hex, piece: Piece):
        if target_hex not in self.board:
            raise ValueError(f"No pieces at cell {target_hex} to remove!")
        self.board[target_hex].append(piece)  # Add the piece to the stack

    def remove_top_piece(self, hex: Hex):
        """
        Removes the top piece from the stack at position (q, r).

        Args:
            q (int): Axial coordinate (column).
            r (int): Axial coordinate (row).

        Returns:
            str: The piece removed from the top of the stack.

        Raises:
            ValueError: If the cell has no pieces.
        """
        if self.hex_empty(hex):
            raise ValueError(f"No pieces at cell {hex} to remove!")
        return self.board[hex].pop()

    def peek_top_piece(self, hex: Hex):
        """
        Peeks at the top piece in the stack at position (q, r) without removing it.

        Args:
            q (int): Axial coordinate (column).
            r (int): Axial coordinate (row).

        Returns:
            str: The piece on top of the stack, or None if the stack is empty.
        """
        if self.hex_empty(hex):
            return None
        return self.board[hex][-1]

    def pieces_count(self, hex: Hex) -> int:
        if self.hex_empty(hex):
            return 0
        return len(self.board[hex])

    def possible_inserts(self, role_type: str, turn: int) -> list[Hex]:
        """available spots to insert a piece"""
        possible_positions = []
        assert role_type in ["black", "white"]

        # Special case for the initial placement
        if turn <= 2:
            if role_type == "white":
                possible_positions = [Hex(0, 0)]
            else:
                possible_positions = Hex(0, 0).generate_adj_hexs()
        else:
            for hex in self.board:
                if self.hex_empty(hex):
                    # Check if the hex is surrounded by pieces of the opposite color
                    is_valid = False
                    for neighbor in hex.generate_adj_hexs():
                        if neighbor not in self.board:
                            continue
                        neighbor_piece = self.peek_top_piece(neighbor)
                        if neighbor_piece is None:
                            continue
                        if neighbor_piece.piece_type == role_type:
                            is_valid = True

                        if neighbor_piece.piece_type != role_type:
                            is_valid = False
                            break

                    if is_valid:
                        possible_positions.append(hex)

        return possible_positions

    def possible_moves(
        self, hex: Hex, role_type: Literal["white", "black"]
    ) -> list[Hex]:
        # no possible location_before queen is set
        queen_location = self.get_queen_location(role_type)
        if queen_location is None:
            return []

        piece: Piece = self.peek_top_piece(hex)
        possible_positions: list[Hex] = []
        if self.pieces_count(hex) <= 1 and not self.can_move_without_breaking_hive(hex):
            return possible_positions

        if isinstance(piece, Queen):
            # Get adjacent hexes
            adjacent_hexes = hex.generate_adj_hexs()

            for adjacent_hex in adjacent_hexes:
                # Check if the hex is empty
                if self.hex_empty(adjacent_hex):
                    # Check if the move doesn't break the hive
                    if self.is_adjacent_to_pieces(adjacent_hex, hex) and self.can_slide(
                        hex, adjacent_hex
                    ):
                        possible_positions.append(adjacent_hex)

        elif isinstance(piece, Ant):
            # BFS to find all reachable hexes
            queue = [hex]
            visited = set()

            while queue:
                current_hex = queue.pop(0)

                # Skip already visited cells
                if current_hex in visited:
                    continue
                visited.add(current_hex)

                # Check all adjacent hexes
                for adj_hex in current_hex.generate_adj_hexs():
                    # Skip the current hex and already visited ones
                    if adj_hex in visited:
                        continue

                    # Check if the hex is empty and adjacent to an occupied cell
                    if (
                        self.hex_empty(adj_hex)
                        and self.is_adjacent_to_pieces(adj_hex, hex)
                        and self.can_slide(current_hex, adj_hex)
                    ):
                        # Ensure moving to this hex doesn't create gaps
                        if self.is_boundary_hex(adj_hex):
                            possible_positions.append(adj_hex)
                            queue.append(
                                adj_hex
                            )  # Continue exploring from this position
        elif isinstance(piece, Beetle):
            # Get adjacent hexes
            adjacent_hexes = hex.generate_adj_hexs()

            for adj_hex in adjacent_hexes:
                # Check if the Beetle is on the ground level or on top of another piece
                if self.hex_empty(adj_hex):
                    # Ground-level move to an empty hex
                    if self.is_adjacent_to_pieces(adj_hex, hex):
                        possible_positions.append(adj_hex)
                else:
                    # Moving on top of the Hive
                    # If there's a stack in the target hex, the Beetle can move on top
                    possible_positions.append(adj_hex)
        elif isinstance(piece, Hopper):
            # Grasshopper movement
            directions = hex.generate_directions()  # Get all six directions
            for direction in directions:
                current_hex = hex
                found_pieces = False  # Ensure the Hopper crosses at least one piece

                while (current_hex + direction) in self.board:
                    # Move in the current direction
                    next_hex = current_hex + direction

                    if next_hex not in self.board:
                        break  # Out of bounds

                    if not self.hex_empty(next_hex):
                        found_pieces = (
                            True  # Mark that at least one piece has been crossed
                        )
                    else:
                        # Found an empty space; if we crossed at least one piece, this is a valid move
                        if found_pieces:
                            possible_positions.append(next_hex)
                        break  # Stop looking further in this direction

                    # Update current_hex to continue in the same direction
                    current_hex = next_hex
        elif isinstance(piece, Spider):
            # Check all hexes on the board
            directions = {
                Hex(0, -1): ((-1, 0), (1, -1)),
                Hex(1, -1): ((0, -1), (1, 0)),
                Hex(1, 0): ((1, -1), (0, 1)),
                Hex(0, 1): ((1, 0), (-1, 1)),
                Hex(-1, 1): ((0, 1), (-1, 0)),
                Hex(-1, 0): ((-1, 1), (0, -1)),
            }
            queue = deque([(hex, 3)])
            visited = set()
            visited.add(hex)
            while queue:
                current_hex, depth = queue.popleft()
                if depth == 0:
                    possible_positions.append(current_hex)
                    continue
                current_neighbors = current_hex.generate_adj_hexs()
                for neighbor in current_neighbors:
                    if self.hex_empty(neighbor) or neighbor in visited:
                        continue
                    dir = neighbor - current_hex
                    adj_directions = directions[dir]
                    for adj_dir in adj_directions:
                        adj_hex = current_hex + Hex(*adj_dir)
                        if (
                            adj_hex in self.board
                            and adj_hex not in visited
                            and self.hex_empty(adj_hex)
                            and self.can_slide(current_hex, adj_hex)
                        ):
                            visited.add(adj_hex)
                            queue.append((adj_hex, depth - 1))
        else:
            raise ValueError("Unknown Piece")
        return possible_positions

    def is_adjacent_to_pieces(self, hex: Hex, original_hex: Hex) -> bool:
        """
        Check if the hex is adjacent to at least one piece
        """
        adjacent = False
        for adj_hex in hex.generate_adj_hexs():
            if (
                adj_hex in self.board
                and adj_hex != original_hex
                and not self.hex_empty(adj_hex)
            ):
                adjacent = True
                break

        return adjacent

    def is_boundary_hex(self, hex: Hex) -> bool:
        """
        Check if a hex is a valid boundary hex for Ant movement.
        A boundary hex is empty and adjacent to at least one occupied hex.
        """
        for adj_hex in hex.generate_adj_hexs():
            if adj_hex in self.board and not self.hex_empty(adj_hex):
                return True
        return False

    def can_move_without_breaking_hive(self, current_hex: Hex) -> bool:
        """
        Check if removing a piece from current_hex would break the hive connectivity
        """
        # If there are no pieces on the board, can't break anything
        if not self.board:
            return True

        # Get all hexes with pieces
        board_hexes = {hex for hex, pieces in self.board.items() if pieces}

        # Remove the current hex
        board_hexes.discard(current_hex)

        # If no hexes left after removal, consider it connected
        if not board_hexes:
            return True

        # Start BFS from an arbitrary hex
        start_hex = next(iter(board_hexes))

        # Perform BFS to check connectivity
        visited = set()
        queue = [start_hex]

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue

            visited.add(current)

            # Get adjacent hexes
            for adj_hex in Hex(current.q, current.r).generate_adj_hexs():
                # Check if adjacent hex has pieces and hasn't been visited
                if adj_hex in board_hexes and adj_hex not in visited:
                    queue.append(adj_hex)

        # Check if all remaining hexes are connected
        return len(visited) == len(board_hexes)

    def get_queen_location(self, role_type: Literal["white", "black"]) -> Hex:
        searched_piece = Queen(role_type)
        for hex, pieces in self.board.items():
            if searched_piece in pieces:
                return hex
        return None

    def is_endgame(self, role_type: Literal["white", "black"]) -> bool:
        queen_location = self.get_queen_location(role_type)
        if queen_location is None:
            return False
        neighbors: list[Hex] = queen_location.generate_adj_hexs()
        return all(not self.hex_empty(neighbor) for neighbor in neighbors)

    def can_slide(self, from_hex: Hex, to_hex: Hex) -> bool:
        """
        Check if a piece can slide from one hex to another without breaking the sliding rule.

        A slide is possible if:
        1. The piece can physically move between two adjacent hexes
        2. The movement doesn't break the sliding requirement
        """
        # Ensure the hexes are adjacent
        if to_hex not in from_hex.generate_adj_hexs():
            return False

        dir_hex = to_hex - from_hex
        dir = (dir_hex.q, dir_hex.r)
        directions = {
            (0, -1): ((-1, 0), (1, -1)),
            (1, -1): ((0, -1), (1, 0)),
            (1, 0): ((1, -1), (0, 1)),
            (0, 1): ((1, 0), (-1, 1)),
            (-1, 1): ((0, 1), (-1, 0)),
            (-1, 0): ((-1, 1), (0, -1)),
        }
        if dir not in directions:
            return False
        counter = 0
        adj_directions = directions[dir]
        for adj_dir in adj_directions:
            adj_hex = from_hex + Hex(*adj_dir)
            if not self.hex_empty(adj_hex):
                counter += 1

        return counter < 2
