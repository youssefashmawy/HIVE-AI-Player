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
    GREY,
    BLACK,
    CYAN,
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

    scaling_factor = 0.8
    scale_width = 1.15
    font = pygame.font.SysFont(None, 24)

    # Draw unplaced pieces (stacks) with counts
    for key, data in board.unplaced_pieces.items():
        position = hex_to_pixel(LAYOUT, data["position"])
        image = piece_images.get(key)
        if image:
            # Scale the image
            piece_width, piece_height = image.get_size()
            scaled_width = int(piece_width * scaling_factor * scale_width)
            scaled_height = int(piece_height * scaling_factor)
            scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

            # Draw the image centered on the hex
            WIN.blit(
                scaled_image,
                (
                    position.x - scaled_width // 2,
                    position.y - scaled_height // 2,
                ),
            )

            # Render and draw the count next to the piece
            count_text = font.render(str(data["count"]), True, BLACK)
            WIN.blit(
                count_text,
                (
                    position.x + scaled_width // 2 - count_text.get_width() // 2,
                    position.y - scaled_height // 2 - count_text.get_height(),
                ),
            )

    # Draw placed pieces without counts
    for piece in board.board:
        position = hex_to_pixel(LAYOUT, piece.hex)
        image_key = f"{piece.piece_type}_{piece.piece_name}"
        image = piece_images.get(image_key)
        if image:
            # Scale the image
            piece_width, piece_height = image.get_size()
            scaled_width = int(piece_width * scaling_factor * scale_width)
            scaled_height = int(piece_height * scaling_factor)
            scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

            # Draw the image centered on the hex
            WIN.blit(
                scaled_image,
                (
                    position.x - scaled_width // 2,
                    position.y - scaled_height // 2,
                ),
            )


def setup_board(board: Board):
    piece_counts = {
        "ant": 3,
        "beetle": 2,
        "queen": 1,
        "grasshopper": 3,
        "spider": 2,
    }

    # Positions for black piece stacks
    black_positions = {
        "ant": Hex(-8, -2),
        "beetle": Hex(-8, 0),
        "queen": Hex(-8, 2),
        "grasshopper": Hex(-8, 4),
        "spider": Hex(-8, 6),
    }

    # Initialize unplaced black pieces
    for name, count in piece_counts.items():
        position = black_positions[name]
        board.unplaced_pieces[f"black_{name}"] = {
            "position": position,
            "count": count,
        }

    # Positions for white piece stacks
    white_positions = {
        "ant": Hex(8, -10),
        "beetle": Hex(8, -8),
        "queen": Hex(8, -6),
        "grasshopper": Hex(8, -4),
        "spider": Hex(8, -2),
    }

    # Initialize unplaced white pieces
    for name, count in piece_counts.items():
        position = white_positions[name]
        board.unplaced_pieces[f"white_{name}"] = {
            "position": position,
            "count": count,
        }


def draw_suggested_moves(moves: list[hex]) -> None:
    for move in moves:
        draw_hex(move, CYAN)
