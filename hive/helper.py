from .layout import Layout
from .point import Point
from .hex import Hex
from math import pi, cos, sin
from .board import Board
from .piece import Piece
import pygame
from .constants import (
    LAYOUT,
    WIN,
    BLUE,
    black_ant,
    black_spider,
    black_queen,
    black_grasshopper,
    black_beetle,
    white_ant,
    white_spider,
    white_queen,
    white_grasshopper,
    white_beetle,
)


def hex_to_pixel(layout: Layout, h: Hex) -> Point:
    m = layout.orientation
    x = (m.f[0] * h.q + m.f[1] * h.r) * layout.size.x
    y = (m.f[2] * h.q + m.f[3] * h.r) * layout.size.y
    return Point(x, y) + layout.origin


def hex_round(coordinates: tuple[float]) -> Hex:
    """rounds hex coordinates

    Args:
        coordinates (tuple[float]): (q, r, s)

    Returns:
        Hex: Hex object having rounded hex coordinates
    """
    q = int(round(coordinates[0]))
    r = int(round(coordinates[1]))
    s = int(round(coordinates[2]))

    q_diff = abs(q - coordinates[0])
    r_diff = abs(r - coordinates[1])
    s_diff = abs(s - coordinates[2])

    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    elif r_diff > s_diff:
        r = -q - s
    else:
        s = -q - r

    return Hex(q, r)


def pixel_to_hex(layout: Layout, p: tuple[int, int]) -> Hex:
    """Returns the center of the hexagonal we currently are at

    Args:
        layout (Layout): Use the constant LAYOUT_FLAT
        p (Point): point clicked by mouse down button

    Returns:
        Hex: center of the hex we are currently at
    """
    m = layout.orientation
    pt = Point(
        ((p[0] - layout.origin.x) / layout.size.x),
        ((p[1] - layout.origin.y) / layout.size.y),
    )
    q = m.b[0] * pt.x + m.b[1] * pt.y
    r = m.b[2] * pt.x + m.b[3] * pt.y
    return hex_round((q, r, -q - r))


def hex_corner_offset(layout: Layout, corner: int) -> Point:
    size = layout.size
    # layout.orientation.start_angle == 0 to make it flat top
    angle = 2.0 * pi * (layout.orientation.start_angle + corner) / 6.0
    return Point(size.x * cos(angle), size.y * sin(angle))


def polygon_corners(layout: Layout, h: Hex) -> list[Point]:
    corners = []
    center = hex_to_pixel(layout, h)
    for i in range(6):
        offset = hex_corner_offset(layout, i)
        # print(f"\n\n{offset}\n\n{center}\n\n")
        corners.append(Point(center.x + offset.x, center.y + offset.y))
    return corners


def draw_hex(
    hex: Hex, color: tuple[int] = BLUE, layout: Layout = LAYOUT, WIN=WIN, width=1
):
    """Draw a single Hexagon on the screen."""
    corners = polygon_corners(layout, hex)
    points = [(corner.x, corner.y) for corner in corners]
    pygame.draw.polygon(WIN, color, points, width)


def draw_pieces(board: Board):
    piece_images = {
        "black_ant": black_ant,
        "black_spider": black_spider,
        "black_queen": black_queen,
        "black_grasshopper": black_grasshopper,
        "black_beetle": black_beetle,
        "white_ant": white_ant,
        "white_spider": white_spider,
        "white_queen": white_queen,
        "white_grasshopper": white_grasshopper,
        "white_beetle": white_beetle,
    }

    for piece in board.board:
        position = hex_to_pixel(LAYOUT, piece.hex)
        image = piece_images.get(f"{piece.piece_type}_{piece.piece_name}")
        if image:
            piece_width, piece_height = image.get_size()
            WIN.blit(
                image,
                (
                    position.x - piece_width // 2,
                    position.y - piece_height // 2,
                ),
            )


def setup_board(board: Board):
    # Place black pieces on the left
    black_positions = [
        Hex(-8, -2),
        Hex(-8, 0),
        Hex(-8, 2),
        Hex(-8, 4),
        Hex(-8, 6),
    ]
    black_piece_names = ["ant", "spider", "queen", "grasshopper", "beetle"]

    for position, name in zip(black_positions, black_piece_names):
        piece = Piece(position, name, "black")
        board.board.append(piece)

    # Place white pieces on the right
    white_positions = [
        Hex(8, -10),
        Hex(8, -8),
        Hex(8, -6),
        Hex(8, -4),
        Hex(8, -2),
    ]
    white_piece_names = ["ant", "spider", "queen", "grasshopper", "beetle"]

    for position, name in zip(white_positions, white_piece_names):
        piece = Piece(position, name, "white")
        board.board.append(piece)
