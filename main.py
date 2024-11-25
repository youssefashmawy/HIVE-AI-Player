import pygame
import math
from hive.constants import (
    FPS,
    LAYOUT,
    BLUE,
    background_image,
    WIN,
)
from hive.helper import *

pygame.init()


pygame.display.set_caption("Hive")
WIN.blit(background_image, (0, 0))


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draw the hex grid
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            hex = pixel_to_hex(LAYOUT, pos)
            draw_hex(hex, BLUE, width=5)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
