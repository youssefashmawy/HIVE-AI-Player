import pygame
from hive.board import Board
from hive.constants import Consts
from hive.hex import Hex
from hive.point import Point
from math import pi, cos, sin
from pygame.rect import Rect


class HiveBoard:
    def __init__(self):
        """
        Initialize the HiveBoard using existing constants
        """
        # Use the existing window and constants
        self.window = Consts.WIN
        self.layout = Consts.LAYOUT
        self._hexes: list[Hex, Rect] = []

        # Piece images dictionary
        self.piece_images = {
            "black_ant": Consts.black_ant,
            "black_spider": Consts.black_spider,
            "black_queen": Consts.black_queen,
            "black_grasshopper": Consts.black_grasshopper,
            "black_beetle": Consts.black_beetle,
            "white_ant": Consts.white_ant,
            "white_spider": Consts.white_spider,
            "white_queen": Consts.white_queen,
            "white_grasshopper": Consts.white_grasshopper,
            "white_beetle": Consts.white_beetle,
        }

        # Drawing parameters
        self.scaling_factor = 0.8
        self.scale_width = 1.15

    def hex_to_pixel(self, h: Hex) -> Point:
        """Convert hex coordinates to pixel coordinates"""
        m = self.layout.orientation
        x = (
            m.f[0] * h.q + m.f[1] * h.r
        ) * self.layout.size.x + self.window.get_width() // 2
        y = (
            m.f[2] * h.q + m.f[3] * h.r
        ) * self.layout.size.y + self.window.get_height() // 2
        return Point(x, y) + self.layout.origin

    def hex_corner_offset(self, corner: int) -> Point:
        """Calculate hex corner offset"""
        size = self.layout.size
        angle = 2.0 * pi * (self.layout.orientation.start_angle + corner) / 6.0
        return Point(size.x * cos(angle), size.y * sin(angle))

    def polygon_corners(self, h: Hex) -> list[Point]:
        """Get polygon corners for a hex"""
        corners = []
        center = self.hex_to_pixel(h)
        for i in range(6):
            offset = self.hex_corner_offset(i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))
        return corners

    def draw_hex(
        self, hex: Hex, color: tuple[int] = Consts.BLUE, width: int = 1
    ) -> Rect:
        """Draw a single hexagon on the screen"""
        corners = self.polygon_corners(hex)
        points = [(corner.x, corner.y) for corner in corners]
        return pygame.draw.polygon(self.window, color, points, width)

    def draw_pieces(self, board: Board):
        """Draw all pieces on the board, accounting for stacks."""
        for hex, stack in board.board.items():
            # Only draw the top piece in the stack
            if stack:
                top_piece = stack[-1]
                position = self.hex_to_pixel(hex)
                image = top_piece.get_image()

                if image:
                    # Scale the image
                    piece_width, piece_height = image.get_size()
                    scaled_width = int(
                        piece_width * self.scaling_factor * self.scale_width
                    )
                    scaled_height = int(piece_height * self.scaling_factor)
                    scaled_image = pygame.transform.scale(
                        image, (scaled_width, scaled_height)
                    )

                    # Draw the image centered on the hex
                    self.window.blit(
                        scaled_image,
                        (
                            position.x - scaled_width // 2,
                            position.y - scaled_height // 2,
                        ),
                    )

    def draw_suggested_moves(self, moves: list[Hex]):
        """Draw suggested moves in cyan"""
        for move in moves:
            self.draw_hex(move, Consts.GREEN, 2)

    def draw(self, board: Board, suggested_moves: list[Hex] = None):
        """
        Draw method compatible with the existing game loop

        Args:
            board (Board): The game board to draw
            suggested_moves (list[Hex], optional): List of possible moves to highlight
        """
        if not self._hexes:
            # Draw all hexes on the board as white initially
            for hex in board.board.keys():
                self._hexes.append(
                    (hex, self.draw_hex(hex, color=Consts.WHITE, width=1))
                )  # Fill white hexagon

            return
        # Draw all hexes on the board as white initially
        for hex in board.board.keys():
            self.draw_hex(hex, color=Consts.WHITE, width=1)  # Fill white hexagon

        # Draw pieces on the board
        self.draw_pieces(board)

        # Draw suggested moves if provided
        if suggested_moves:
            self.draw_suggested_moves(suggested_moves)

    def handle_click(self, pos: tuple[int, int]) -> Hex:
        """
        Checks if a click occurred on a hex and returns the corresponding Hex object.

        Args:
            pos: A tuple representing the click coordinates (x, y).

        Returns:
            The clicked Hex object if found, otherwise None.
        """

        for hex, rect in self._hexes:
            # Assuming each hex has a `rect` attribute representing its bounding box
            if rect.collidepoint(pos):
                return hex

        return None
