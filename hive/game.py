import pygame
import sys
from typing import Optional, Tuple
from typing import Literal

from hive.constants import Consts
from hive.board import Board
from hive.hex import Hex
from hive.piece import Ant, Hopper, Queen, Beetle, Spider, Piece
from hive.AIGame import HiveMinMaxAI

from hive.ui.inventory import Inventory, Item
from hive.ui.board import HiveBoard


class HiveGame:
    def __init__(self, game_config: dict):
        """
        Initialize the Hive game with given configuration

        :param game_config: Dictionary containing game settings
        """

        # Existing initialization...
        self.game_config = game_config

        # AI Player Setup
        self.white_ai = None
        self.black_ai = None

        mode = game_config.get("mode", "Player vs Player")

        # Configure AI players based on mode
        if mode == "AI vs Player":
            self.black_ai = HiveMinMaxAI(
                role="black",
                difficulty=game_config.get("difficulty_1", "medium"),
            )
        elif mode == "AI vs AI":
            self.white_ai = HiveMinMaxAI(
                role="white",
                difficulty=game_config.get("difficulty_1", "medium"),
            )
            self.black_ai = HiveMinMaxAI(
                role="black",
                difficulty=game_config.get("difficulty_2", "medium"),
            )

        # Game state variables
        self.clock = pygame.time.Clock()

        self.hive_board = HiveBoard()

        self.board = Board(7)
        self.game_config = game_config

        # Player interaction variables
        self.selected_outside_item: Item = None
        self.selected_piece_hex: Hex = None

        self.possible_moves: list[Hex] = []

        # Game mode settings
        self.game_mode = game_config.get("mode", "player_vs_player")
        self.current_player = "white"  # Starting player

        # Initialize inventories
        self.white_inventory = Inventory(
            0, Consts.WIN.get_height() - Consts.INVENTORY_HEIGHT, "white"
        )
        self.black_inventory = Inventory(
            480, Consts.WIN.get_height() - Consts.INVENTORY_HEIGHT, "black"
        )

        self.setup_inventories()
        self.turn = 1  # odd means white and even means black

        # initialize skip_counter 
        self.white_skip_counter = 0
        self.black_skip_counter = 0

    def is_role_white(self):
        return self.turn % 2 == 1

    def setup_inventories(self):
        """
        Setup the inventories with unplaced pieces for both players.
        """
        white_piece_images = {
            "Ant": Consts.white_ant,
            "Beetle": Consts.white_beetle,
            "Queen": Consts.white_queen,
            "Hopper": Consts.white_grasshopper,
            "Spider": Consts.white_spider,
        }

        black_piece_images = {
            "Ant": Consts.black_ant,
            "Beetle": Consts.black_beetle,
            "Queen": Consts.black_queen,
            "Hopper": Consts.black_grasshopper,
            "Spider": Consts.black_spider,
        }
        piece_counts = {
            "Queen": 1,
            "Spider": 2,
            "Beetle": 2,
            "Ant": 3,
            "Hopper": 3,
        }

        # Populate white inventory
        for name, count in piece_counts.items():
            self.white_inventory.add_item(
                Item("white", name, count, white_piece_images[name])
            )

        # Populate black inventory
        for name, count in piece_counts.items():
            self.black_inventory.add_item(
                Item("black", name, count, black_piece_images[name])
            )

    def handle_events(self,events:list[pygame.event.Event]) -> bool:
        """
        Handle pygame events

        :return: Boolean indicating if there's a change in game state
        """

        for event in events:
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # handle inventory clicks
                white_inventory_selected_item: Item = self.white_inventory.handle_click(
                    event.pos
                )
                black_inventory_selected_item: Item = self.black_inventory.handle_click(
                    event.pos
                )
                if white_inventory_selected_item and self.is_role_white():
                    self.white_inventory.reset_selected()
                    self.black_inventory.reset_selected()
                    self.possible_moves = []
                    # if the turn = 7 (4th white turn) then ignore any piece other than queen
                    # if its already placed then continue as normal
                    if (
                        self.turn == 7
                        and self.board.get_queen_location("white") is None
                        and white_inventory_selected_item.name != "Queen"
                    ):
                        break

                    self.white_inventory.select(white_inventory_selected_item)
                    self.selected_outside_item = white_inventory_selected_item
                    self.possible_moves = self.board.possible_inserts(
                        "white", self.turn
                    )
                    self.selected_piece_hex = None

                if black_inventory_selected_item and not self.is_role_white():
                    self.white_inventory.reset_selected()
                    self.black_inventory.reset_selected()
                    self.possible_moves = []
                    # if the turn = 8 (4th black turn) then ignore any piece other than queen
                    # if its already placed then continue as normal
                    if (
                        self.turn == 8
                        and self.board.get_queen_location("black") is None
                        and black_inventory_selected_item.name != "Queen"
                    ):
                        break
                    self.black_inventory.select(black_inventory_selected_item)
                    self.selected_outside_item = black_inventory_selected_item
                    self.possible_moves = self.board.possible_inserts(
                        "black", self.turn
                    )
                    self.selected_piece_hex = None

                # handle grid clicks
                board_hex = self.hive_board.handle_click(event.pos)

                if board_hex and board_hex in self.possible_moves:
                    # if it come from outside pieces or inside

                    if self.selected_outside_item is not None:
                        self.board.place_piece(
                            board_hex,
                            self.get_piece_from_item(self.selected_outside_item),
                        )
                        self.selected_outside_item.count -= 1
                        self.selected_outside_item = None

                    if self.selected_piece_hex is not None:
                        self.board.place_piece(
                            board_hex,
                            self.board.remove_top_piece(self.selected_piece_hex),
                        )
                        self.selected_piece_hex = None

                    self.white_inventory.reset_selected()
                    self.black_inventory.reset_selected()
                    self.possible_moves = []
                    return True

                if (
                    board_hex
                    and not self.board.hex_empty(board_hex)
                    and self.board.peek_top_piece(board_hex).piece_type
                    == self.get_type_from_turn()
                ):
                    self.white_inventory.reset_selected()
                    self.black_inventory.reset_selected()
                    self.possible_moves = self.board.possible_moves(
                        board_hex, self.get_type_from_turn()
                    )
                    self.selected_outside_item = None
                    self.selected_piece_hex = board_hex

        return False

    def get_piece_from_item(self, item: Item) -> Item:
        if item is None:
            raise ValueError("None Item:")

        if item.name == "Ant":
            return Ant(item.type)
        elif item.name == "Beetle":
            return Beetle(item.type)
        elif item.name == "Queen":
            return Queen(item.type)
        elif item.name == "Hopper":
            return Hopper(item.type)
        elif item.name == "Spider":
            return Spider(item.type)

        raise ValueError("Unknown Item: " + item)

    def get_type_from_turn(self):
        return "white" if self.is_role_white() else "black"

    def update_display(self):
        """
        Update the game display
        """
        Consts.WIN.blit(Consts.background_image, (0, 0))

        self.hive_board.draw(self.board, self.possible_moves)

        self.white_inventory.draw(Consts.WIN)  # Draw white inventory
        Consts.WIN.blit(
            Consts.logo_image, (360, Consts.WIN.get_height() - Consts.INVENTORY_HEIGHT)
        )
        self.black_inventory.draw(Consts.WIN)  # Draw black inventory

        # Draw role indicator
        font = pygame.font.Font(None, 24)
        role_text = font.render("Role:", True, (0, 0, 0))
        role_text_rect = role_text.get_rect(topleft=(10, 10))
        Consts.WIN.blit(role_text, role_text_rect)

        # Draw colored circle to indicate current role
        circle_color = (0, 0, 0) if self.get_type_from_turn() == "black" else (255, 255, 255)
        circle_outline_color = (255, 255, 255) if self.get_type_from_turn() == "black" else (0, 0, 0)
        pygame.draw.circle(Consts.WIN, circle_outline_color, (role_text_rect.right + 20, role_text_rect.centery), 12, 2)
        pygame.draw.circle(Consts.WIN, circle_color, (role_text_rect.right + 20, role_text_rect.centery), 10)

        pygame.display.update()

    def run_game(self) -> Literal["white", "black", "draw"]:
        """
        Main game loop

        :return: Boolean indicating if the game should continue
        """
        # Reset game state

        while True:
            events=pygame.event.get()

            end_game_result = self.end_game_result(events)
            if end_game_result:
                return end_game_result

            current_player = self.get_type_from_turn()

            # Handle AI turns
            if current_player == "white" and self.white_ai:
                # white doesn't have any moves so skip
                if not self.perform_ai_move(self.white_ai):
                    self.display_skip_screen()

                self.turn += 1
            elif current_player == "black" and self.black_ai:
                # black doesn't have any moves so skip
                if not self.perform_ai_move(self.black_ai):
                    self.display_skip_screen()

                self.turn += 1
                # if the other player is player not ai, check for the new turn if it has possible moves or skip
                if self.white_ai is None and self.is_turn_skippable(self.turn):
                    self.display_skip_screen()
                    self.turn += 1
            else:
                # Handle human turn
                turn_flipped = self.handle_events(events)
                if turn_flipped:
                    self.turn += 1
                    if self.black_ai is None and self.is_turn_skippable(self.turn):
                        self.display_skip_screen()
                        self.turn += 1

            # Update display
            self.update_display()

            # Control game speed
            self.clock.tick(Consts.FPS)


    def end_game_result(self,events:list[pygame.event.Event]) -> Literal["white", "black", "draw","exit", None]:
        white_win = self.board.is_endgame("black")  # white wins if black is gameover
        black_win = self.board.is_endgame("white")  # black wins if white is gameover
        
        if white_win and black_win:
            return "draw"
        if white_win:
            return "white"
        if black_win:
            return "black"

        if self.white_skip_counter >= 3:
            return "black"
        if self.black_skip_counter >= 3:
            return "white"
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # 'm' to get menu
                    return "exit"  
            
        return None

    def perform_ai_move(self, ai_player: HiveMinMaxAI):
        """
        Use the AI player to decide and execute the best move.

        :param ai_player: Instance of HiveMinMaxAI
        """
        inventory = (
            self.white_inventory if ai_player.role == "white" else self.black_inventory
        )

        best_move = ai_player.choose_best_move(
            self.board,
            self.turn,
            self.white_inventory.items,
            self.black_inventory.items,
        )

        if best_move:

            move_type = best_move["type"]
            if move_type == "move":
                moved_piece = self.board.remove_top_piece(best_move["from_hex"])
                self.board.place_piece(best_move["to_hex"], moved_piece)
            else:
                item = inventory.get_item_by_name(best_move["piece"])
                if item and item.count > 0:
                    self.board.place_piece(
                        best_move["to_hex"], self.get_piece_from_item(item)
                    )
                    item.count -= 1
                else:
                    raise ValueError(
                        f"AI attempted to place a piece of type '{best_move['piece']}', but it's unavailable in the inventory."
                    )
            return True
        else:
            return False
    
    def _is_turn_skippable_helper(self, turn: int) -> bool:
        """
        Check if the current player has no legal moves to make.

        :return: Boolean indicating if the turn should be skipped
        """
        current_player = "white" if turn % 2 == 1 else "black"
        inventory = (
            self.white_inventory if current_player == "white" else self.black_inventory
        )
        inventory = inventory.items

        # Check if any pieces can be inserted
        possible_inserts = self.board.possible_inserts(current_player, turn)
        if possible_inserts:
            for item in inventory:
                if item.count > 0:
                    return False

        # Check if any existing pieces can be moved
        for hex_pos in self.board.board:
            piece = self.board.peek_top_piece(hex_pos)
            if piece and piece.piece_type == current_player:
                if self.board.possible_moves(hex_pos, current_player):
                    return False

        return True
    
    def is_turn_skippable(self, turn:int)->bool:
        res=self._is_turn_skippable_helper(turn)
        if res:
            if self.is_role_white():
                self.white_skip_counter +=1
            else:
                self.black_skip_counter +=1
        else:
            self.white_skip_counter = 0
            self.black_skip_counter = 0

        # return the actual result
        return res
       
    def display_skip_screen(self):
        """
        Display a screen asking the player to confirm skipping their turn.
        """
        if self.is_role_white():
            self.white_skip_counter += 1
        else:
            self.black_skip_counter += 1
        # Create a semi-transparent overlay
        overlay = pygame.Surface(Consts.WIN.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        Consts.WIN.blit(overlay, (0, 0))

        # Render text
        font = pygame.font.Font(None, 36)
        current_player = self.get_type_from_turn()
        text_lines = [
            f"{current_player.capitalize()} player has no legal moves!",
            "Press SPACE to skip turn",
        ]

        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                center=(
                    Consts.WIN.get_width() // 2,
                    Consts.WIN.get_height() // 2 + i * 50,
                )
            )
            Consts.WIN.blit(text_surface, text_rect)

        pygame.display.update()
        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Skip turn
                        return True
            self.clock.tick(Consts.FPS)

        return True
