import pygame
import math
from hive.constants import (
    WIDTH,
    HEIGHT,
    FPS,
    LAYOUT_FLAT,
    BLACK,
    GRID_WIDTH,
    GRID_HEIGHT,
    HEX_RADIUS,
    LAYOUT,
    WHITE,
    RED,
    background_image,
)
from hive.helper import *

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Hive")


def draw_hex(hex: Hex, color: tuple[int] = BLACK, layout: Layout = LAYOUT, WIN=WIN):
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

        # WIN.blit(background_image, (0, 0))

        # Draw the hex grid
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            hex = pixel_to_hex(LAYOUT, pos)
            draw_hex(hex, RED)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
