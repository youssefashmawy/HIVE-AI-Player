import pygame
import math
from hive.constants import WIDTH, HEIGHT, FPS, LAYOUT_FLAT, BLACK
from hive.helper import *

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Hive")

GRID_WIDTH = 8
GRID_HEIGHT = 8
HEX_RADIUS = 30
layout = Layout(
    LAYOUT_FLAT,
    Point(HEX_RADIUS, HEX_RADIUS),
    Point(WIDTH // 2, HEIGHT // 2),
)


def draw_hex(hex: Hex, color: tuple[int] = BLACK, layout: Layout = layout, WIN=WIN):
    """Draw a single Hexagon on the screen."""
    corners = polygon_corners(layout, hex)
    points = [(corner.x, corner.y) for corner in corners]
    pygame.draw.polygon(WIN, color, points, 1)


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        WIN.fill((0, 0, 0))

        # Draw the hex grid
        for q in range(-GRID_WIDTH // 2, GRID_WIDTH // 2):
            for r in range(-GRID_HEIGHT // 2, GRID_HEIGHT // 2):
                hex = Hex(q, r)
                color = (255, 255, 255)  # White color for the grid
                draw_hex(hex, color)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
