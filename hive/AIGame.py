from typing import Literal
from typing import List, Optional, Dict, Any,Generator
import random
from hive.piece import Ant, Beetle, Queen, Hopper, Spider, Piece
from hive.board import Board
from hive.hex import Hex

from hive.ui.inventory import Inventory, Item
# import cProfile
# import pstats

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

    def is_queen_placed(self):
        return self.board.get_queen_location(self.get_type_from_turn()) is not None
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
            if not self.board.hex_inside_board(from_hex) or self.board.hex_empty(from_hex):
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
            
            if piece.piece_name == "Queen":
                self.board.white_queen_location=None

            # update the inventory
            for item in self.white_inventory:
                if item.name == piece.piece_name:
                    item.count += 1
                    break
        elif isinstance(from_location, str) and from_location == "black":
            piece = self.board.remove_top_piece(to_location)

            if piece.piece_type != "black":
                raise Exception("Piece in the to location is not black")
            
            if piece.piece_name == "Queen":
                self.board.black_queen_location=None
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
    def __init__(self, role: str, difficulty: Literal["easy", "medium", "hard"]):
        """
        Initialize the MinMax AI for Hive

        :param role: AI's color ('white' or 'black')
        :param max_depth: Maximum search depth for the algorithm
        """
        self.role = role
        difficulty = difficulty.lower()
        self.difficulty = difficulty
        self.max_depth = 1 if difficulty == "easy" else 2 if difficulty == "medium" else 3


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
        # profiler = cProfile.Profile()
        # profiler.enable()
        
        
        undo_stack: list[tuple[str | Hex, Hex]] = []
        node = Node(board, white_inventory, black_inventory, turn)

        best_move = None

        alpha = -1000
        beta = 1000
        for i, move in enumerate(self._generate_all_moves(node)):

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
            if eval_score > alpha:
                alpha = eval_score
                best_move = move

            if beta <= alpha:
                break
        
        # profiler.disable()
        # stats = pstats.Stats(profiler)
        # stats.sort_stats("tottime")  # Sort by cumulative time
        # stats.print_stats(100)  # Print top 20 time-consuming functions
        return best_move

    def _minmax(self, node: Node, depth, is_maximizing, alpha, beta, undo_stack):

        if depth == 0 or node.board.is_endgame("white") or node.board.is_endgame("black"):
            return self._evaluate_board(node)

        if is_maximizing:
            for move in self._generate_all_moves(node):
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
                node.undo_move(undo_stack)

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return alpha
        else:
            for move in self._generate_all_moves(node):
                node.apply_move(
                    move.get("from_hex", None),
                    move.get("to_hex", None),
                    move.get("piece", None),
                    undo_stack,
                )
                eval_score = self._minmax(
                    node, depth - 1, True, alpha, beta, undo_stack
                )
                node.undo_move(undo_stack)

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return beta

    def _generate_all_moves(self, node: Node) -> Generator[Dict[str, Any],None,None]:
        """
        Generate all possible moves for the current player

        :param board: Current game board
        :param turn: Current turn number
        :param inventory: Current player's inventory
        :return: List of possible moves
        """

        # Generate placement moves
        possible_placements = node.board.possible_inserts(
            node.get_type_from_turn(), node.turn
        )

        inventory= node.get_inventory_from_turn()
        if (node.turn == 7 or node.turn == 8) and not node.is_queen_placed():
            for hex in possible_placements:
                yield {"type": "place", "piece": "Queen", "to_hex": hex}
        else:
            for hex in possible_placements:
                # check if it turn is 7 or 8 and the queen is not there 
                for item in inventory:
                    if item.count > 0:
                        yield {"type": "place", "piece": item.name, "to_hex": hex}

        # Generate movement moves
        for hex, pieces in node.board.board.items():
            if pieces and pieces[-1].piece_type == node.get_type_from_turn():
                possible_moves = node.board.possible_moves(
                    hex, node.get_type_from_turn()
                )
                for move_hex in possible_moves:
                    if move_hex in node.board.board:
                        yield {"type": "move", "from_hex": hex, "to_hex": move_hex}
        

    # Dynamic mobility weights based on game turn
    def _calculate_dynamic_weights(self,turn):
        """
        Calculate mobility weights that change throughout the game
        
        Early game (turns 1-6): Focus on piece placement and queen protection
        Mid game (turns 7-12): Balanced mobility and strategic positioning
        Late game (turns 13+): Aggressive mobility and queen threat
        """
        if turn <= 12:
            # Early game: Prioritize queen and strategic piece placement
            return {
                "Beetle": 3,  # Can block and protect queen
                "Hopper": 2,  # Limited but strategic placement
                "Spider": 2,  # Careful movement
                "Ant": 1,  # Less important early
            }
        elif turn <= 24:
            # Mid game: Balanced approach
            return {
                "Ant": 5,  # Increasing mobility importance
                "Spider": 4,  # Strategic movement
                "Beetle": 3,  # Flexible positioning
                "Hopper": 2,  # Situational utility
            }
        else:
            # Late game: Aggressive mobility and queen threat
            return {
                "Ant": 6,  # Maximum mobility crucial
                "Spider": 5,  # Complex movement
                "Beetle": 4,  # Blocking and attacking
                "Hopper": 3,  # More strategic importance
            }
            
    def _evaluate_board(self, node: Node):
        """
        Advanced board evaluation with multiple heuristics

        Heuristics include:
        1. Queen bee safety
        2. end game detection
        3. dynamic wights (early,mid,late)
        4. mobility score
        5. active pieces count
        6. random small noise to prevent infinti loops in AI vs AI
        """
        score = 0
        board = node.board
        role = self.role
        opponent_role = "black" if role == "white" else "white"

        # 2. Queen Bee Safety Heuristic
        around_queen_role = self._around_queen(board, role)
        around_queen_opponent = self._around_queen(board, opponent_role)

        score += (around_queen_opponent-around_queen_role) * 10
        
        if around_queen_opponent == 6:
            return 1000
        
        # Get current turn-based weights
        current_weights = self._calculate_dynamic_weights(node.turn)

        pieces_mobility = self._calculate_pieces_mobility(board)
        # Calculate mobility score
        for (color, piece_type), mobility in pieces_mobility.items():
            # Apply weight based on the piece type
            weight = current_weights.get(piece_type, 1)
            
            # Adjust score based on mobility and color
            if color == role:
                score += mobility * weight
            else:
                score -= mobility * weight

        # Calculate active count
        pieces_active = self._calculate_pieces_active_count(board)
        for (color, piece_type), mobility in pieces_active.items():
            # Apply count based on the piece type
            count = current_weights.get(piece_type, 1)
            
            # Adjust score based on count and color
            if color == role:
                score += count * weight
            else:
                score -= count * weight

        # add random noise between -5 and 0 for ai vs ai
        score += random.randint(-5, 0)

        return score 

    def _calculate_pieces_mobility(self, board: Board):
        """
        Calculate the mobility score for each piece type for a given role using threading
        """
        # Initialize pieces_mobility dictionary
        pieces_mobility = {
            ("black", "Hopper"): 0,
            ("black", "Spider"): 0,
            ("white", "Hopper"): 0,
            ("white", "Spider"): 0,
        }
        
        def calculate_piece_mobility(hex_key):
            """
            Calculate mobility for a specific hex
            
            :param hex_key: The hex coordinate to check
            :return: Tuple of mobility updates or None if no update needed
            """
            if board.hex_empty(hex_key):
                return None
            
            piece = board.board[hex_key][-1]
            mobility_key = (piece.piece_type, piece.piece_name)
            
            # Only process pieces we're tracking
            if mobility_key not in pieces_mobility:
                return None
            
            # Calculate possible moves for this piece
            possible_moves = len(board.possible_moves(hex_key, piece.piece_type))
            
            return (mobility_key, possible_moves)
        
        for hex_key in board.board.keys():
            res= calculate_piece_mobility(hex_key)
            if res is None:
                continue
            mobility_key, moves = res
            pieces_mobility[mobility_key] += moves
        
        return pieces_mobility
    
    def _calculate_pieces_active_count(self, board: Board):
        """
        Calculate the mobility score for each piece type for a given role using threading
        """
        # Initialize pieces_mobility dictionary
        pieces_active = {
            ("black", "Ant"): 0,
            ("black", "Beetle"): 0,
            ("white", "Ant"): 0,
            ("white", "Beetle"): 0,
        }
        
        def calculate_piece_active_count(hex_key):
            """
            Calculate mobility for a specific hex
            
            :param hex_key: The hex coordinate to check
            :return: Tuple of mobility updates or None if no update needed
            """
            if board.hex_empty(hex_key):
                return None
            
            piece = board.board[hex_key][-1]
            active_key = (piece.piece_type, piece.piece_name)
            
            # Only process pieces we're tracking
            if active_key not in pieces_active:
                return None
            
            is_active= board.can_move_without_breaking_hive(hex_key)
            
            return (active_key, 1 if is_active else 0)
        
        for hex_key in board.board.keys():
            res= calculate_piece_active_count(hex_key)
            if res is None:
                continue
            active_key, moves = res
            pieces_active[active_key] += moves
        
        return pieces_active
    def _around_queen(self, board: Board, role):
        """
        Evaluate the safety of the Queen Bee
        """
        queen_location = board.get_queen_location(role)

        if queen_location is None:
            return 0  # Queen not placed yet

        # Check surrounding hexes
        adjacent_hexes = queen_location.generate_adj_hexs()
        blocked_hexes = sum(1 for hex in adjacent_hexes if not board.hex_inside_board(hex) or not board.hex_empty(hex))

        # The more blocked hexes around the queen, the worse the safety
        return blocked_hexes
