import concurrent.futures
import math
from typing import List, Optional, Dict, Any
from copy import deepcopy
from hive.piece import Ant, Beetle, Queen, Hopper, Spider, Piece
from hive.board import Board
from hive.hex import Hex

from hive.ui.inventory import Inventory, Item


class Node:
    def __init__(
        self,
        board: Board,
        white_inventory: list[Item],
        black_inventory: list[Item],
        turn: int,
    ):
        self.board: Board = board
        self.white_inventory: list[Item] = white_inventory
        self.black_inventory: list[Item] = black_inventory
        self.turn: int = turn

    def is_role_white(self):
        return self.turn % 2 == 1

    def get_type_from_turn(self):
        return "white" if self.is_role_white() else "black"

    def get_inventory_from_turn(self):
        return self.white_inventory if self.is_role_white() else self.black_inventory

    def _create_piece(self, piece_type, role) -> Piece:
        """
        Create a piece based on type and role

        :param piece_type: Type of piece to create
        :param role: Color of the piece
        :return: Piece instance
        """
        piece_map = {
            "Ant": Ant,
            "Beetle": Beetle,
            "Queen": Queen,
            "Hopper": Hopper,
            "Spider": Spider,
        }

        return piece_map[piece_type](role)

    def apply_move(
        self,
        from_hex: Hex,
        to_hex: Hex,
        from_inventory_piece_name: str,
        undo_stack: list[tuple[str | Hex, Hex]],
    ):
        # comes from the inventory if the from is none
        if from_hex is None:
            # Save state for undo
            undo_stack.append(
                (
                    self.get_type_from_turn(),
                    to_hex,
                )
            )

            # Place the piece
            piece = self._create_piece(
                from_inventory_piece_name, self.get_type_from_turn()
            )
            self.board.place_piece(to_hex, piece)

            inventory = self.black_inventory
            if self.is_role_white():
                inventory = self.white_inventory

            # Update inventory
            for item in inventory:
                if item.name == from_inventory_piece_name:
                    if item.count > 0:
                        item.count -= 1
                        break
                    else:
                        raise Exception(
                            "No more pieces in inventory: " + from_inventory_piece_name
                        )
        else:
            if self.board.hex_empty(from_hex):
                raise Exception("No piece in the from hex")

            # Save state for undo
            undo_stack.append((from_hex, to_hex))

            # Move the piece
            piece = self.board.remove_top_piece(from_hex)
            self.board.place_piece(to_hex, piece)

        self.turn += 1

    def undo_move(self, undo_stack: list[tuple[str | Hex, Hex]]):
        if not undo_stack:
            raise Exception("No moves to undo")

        from_location, to_location = undo_stack.pop()
        if isinstance(from_location, str) and from_location == "white":
            piece = self.board.remove_top_piece(to_location)
            if piece.piece_type != "white":
                raise Exception("Piece in the to location is not white")
            # update the inventory
            for item in self.white_inventory:
                if item.name == piece.piece_name:
                    item.count += 1
                    break
        elif isinstance(from_location, str) and from_location == "black":
            piece = self.board.remove_top_piece(to_location)

            if piece.piece_type != "black":
                raise Exception("Piece in the to location is not black")
            # update the inventory
            for item in self.black_inventory:
                if item.name == piece.piece_name:
                    item.count += 1
                    break
        else:
            piece = self.board.remove_top_piece(to_location)
            self.board.place_piece(from_location, piece)

        self.turn -= 1


class HiveMinMaxAI:
    def __init__(self, role: str, max_depth: int):
        """
        Initialize the MinMax AI for Hive

        :param role: AI's color ('white' or 'black')
        :param max_depth: Maximum search depth for the algorithm
        """
        self.role = role
        self.max_depth = max_depth

    def choose_best_move(
        self,
        board: Board,
        turn: int,
        white_inventory: list[Item],
        black_inventory: list[Item],
    ):
        """
        Choose the best move using MinMax with Alpha-Beta pruning.

        :param board: Current game board
        :param turn: Current turn number
        :param white_inventory: Inventory of white pieces
        :param black_inventory: Inventory of black pieces
        :return: Best move dictionary
        """
        undo_stack: list[tuple[str | Hex, Hex]] = []
        node = Node(board, white_inventory, black_inventory, turn)

        best_move = None
        best_eval = float("-inf")

        moves = self._generate_all_moves(node)

        if not moves:
            return None

        alpha = float("-inf")
        beta = float("inf")
        for i, move in enumerate(moves):

            # Apply the move
            node.apply_move(
                move.get("from_hex", None),
                move.get("to_hex", None),
                move.get("piece", None),
                undo_stack,
            )

            # Evaluate the move - always minimize for opponent
            eval_score = self._minmax(
                node, self.max_depth - 1, False, alpha, beta, undo_stack
            )

            # Undo the move
            node.undo_move(undo_stack)

            # Always maximize for the AI's own role
            if eval_score > best_eval:
                best_eval = eval_score
                best_move = move

            if best_eval > alpha:
                alpha = best_eval

            if beta <= alpha:
                break

        return best_move

    def _minmax(self, node: Node, depth, is_maximizing, alpha, beta, undo_stack):

        if depth == 0:
            return self._evaluate_board(node)

        moves = self._generate_all_moves(node)

        if is_maximizing:
            max_eval = float("-inf")
            for move in moves:
                # Apply the move
                node.apply_move(
                    move.get("from_hex", None),
                    move.get("to_hex", None),
                    move.get("piece", None),
                    undo_stack,
                )

                eval_score = self._minmax(
                    node, depth - 1, False, alpha, beta, undo_stack
                )

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, max_eval)
                node.undo_move(undo_stack)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in moves:
                node.apply_move(
                    move.get("from_hex", None),
                    move.get("to_hex", None),
                    move.get("piece", None),
                    undo_stack,
                )
                eval_score = self._minmax(
                    node, depth - 1, True, alpha, beta, undo_stack
                )

                min_eval = min(min_eval, eval_score)
                beta = min(beta, min_eval)
                node.undo_move(undo_stack)
                if beta <= alpha:
                    break
            return min_eval

    def _generate_all_moves(self, node: Node) -> List[Dict[str, Any]]:
        """
        Generate all possible moves for the current player

        :param board: Current game board
        :param turn: Current turn number
        :param inventory: Current player's inventory
        :return: List of possible moves
        """
        moves = []

        # Generate placement moves
        possible_placements = node.board.possible_inserts(
            node.get_type_from_turn(), node.turn
        )
        for hex in possible_placements:
            for item in node.get_inventory_from_turn():
                if item.count > 0:
                    moves.append({"type": "place", "piece": item.name, "to_hex": hex})

        # Generate movement moves
        for hex, pieces in node.board.board.items():
            if pieces and pieces[-1].piece_type == node.get_type_from_turn():
                possible_moves = node.board.possible_moves(
                    hex, node.get_type_from_turn()
                )
                for move_hex in possible_moves:
                    if move_hex in node.board.board:
                        moves.append(
                            {"type": "move", "from_hex": hex, "to_hex": move_hex}
                        )

        return moves

    def _evaluate_board(self, node: Node):
        """
        Advanced board evaluation with multiple heuristics

        Heuristics include:
        1. Piece mobility for each piece type
        2. Queen bee safety
        3. Overall piece mobility
        4. Strategic piece placement
        5. Winning condition detection
        """
        score = 0
        board = node.board
        role = self.role
        opponent_role = "black" if role == "white" else "white"

        # Piece type mobility weights (higher means more strategic importance)
        mobility_weights = {
            "Ant": 4,  # Highly mobile
            "Spider": 3,  # Strategic movement
            "Beetle": 2,  # Can climb and block
            "Hopper": 1,  # Limited mobility
        }

        # 1. Piece Mobility Heuristics
        role_mobility = self._calculate_piece_mobility(board, role, mobility_weights)
        opponent_mobility = self._calculate_piece_mobility(
            board, opponent_role, mobility_weights
        )

        score += role_mobility - opponent_mobility

        # 2. Queen Bee Safety Heuristic
        role_queen_safety = self._evaluate_queen_safety(board, role)
        opponent_queen_safety = self._evaluate_queen_safety(board, opponent_role)

        score += (role_queen_safety - opponent_queen_safety) * 3

        # 4. Endgame Detection (Massive score adjustment)
        if board.is_endgame(role):
            score += 1000  # Winning condition
        elif board.is_endgame(opponent_role):
            score -= 1000  # Losing condition

        return score

    def _calculate_piece_mobility(self, board: Board, role, mobility_weights):
        """
        Calculate mobility score for each piece type for a given role
        """
        total_mobility = 0
        piece_types = ["Ant", "Spider", "Hopper"]

        for piece_type in piece_types:
            # Find all pieces of this type for the given role
            type_pieces = [
                hex
                for hex, pieces in board.board.items()
                if pieces
                and pieces[-1].piece_type == role
                and pieces[-1].piece_name == piece_type
            ]

            # Calculate mobility for each piece
            type_mobility = sum(
                len(board.possible_moves(hex, role)) * mobility_weights[piece_type]
                for hex in type_pieces
            )

            total_mobility += type_mobility

        return total_mobility

    def _evaluate_queen_safety(self, board: Board, role):
        """
        Evaluate the safety of the Queen Bee
        """
        queen_location = board.get_queen_location(role)

        if queen_location is None:
            return 0  # Queen not placed yet

        # Check surrounding hexes
        adjacent_hexes = queen_location.generate_adj_hexs()
        blocked_hexes = sum(1 for hex in adjacent_hexes if not board.hex_empty(hex))

        # The more blocked hexes around the queen, the worse the safety
        return 6 - blocked_hexes
