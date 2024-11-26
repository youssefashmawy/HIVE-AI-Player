import pygame
from hive.constants import (
    FPS,
    LAYOUT,
    BLUE,
    background_image,
    WIN,
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
from hive.helper import *

pygame.init()

pygame.display.set_caption("Hive")
WIN.blit(background_image, (0, 0))


def draw_pieces():

    # Define positions for black pieces (left side)

    black_positions = [
        (50, 50),
        (50, 150),
        (50, 250),
        (50, 350),
        (50, 450),
    ]

    # Define positions for white pieces (right side)
    white_positions = [
        (700, 50),
        (700, 150),
        (700, 250),
        (700, 350),
        (700, 450),
    ]

    # Draw black pieces
    WIN.blit(black_ant, black_positions[0])
    WIN.blit(black_spider, black_positions[1])
    WIN.blit(black_queen, black_positions[2])
    WIN.blit(black_grasshopper, black_positions[3])
    WIN.blit(black_beetle, black_positions[4])

    # Draw white pieces
    WIN.blit(white_ant, white_positions[0])
    WIN.blit(white_spider, white_positions[1])
    WIN.blit(white_queen, white_positions[2])
    WIN.blit(white_grasshopper, white_positions[3])
    WIN.blit(white_beetle, white_positions[4])


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draw the background and pieces
        draw_pieces()

        # Draw the hex grid
        if event.type == pygame.MOUSEBUTTONDOWN:  # Change later
            pos = pygame.mouse.get_pos()
            hex = pixel_to_hex(LAYOUT, pos)
            print(hex)
            draw_hex(hex, BLUE, width=5)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
