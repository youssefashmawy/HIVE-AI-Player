import pygame

WIDTH, HEIGHT = 800, 600

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

FPS = 60

# Images

# Black pieces
black_ant = pygame.transform.scale(pygame.image.load("Assets/black_ant.png"), (44, 24))
black_spider = pygame.transform.scale(
    pygame.image.load("Assets/black_spider.png"), (44, 24)
)
black_queen = pygame.transform.scale(
    pygame.image.load("Assets/black_queen.png"), (44, 24)
)
black_grasshopper = pygame.transform.scale(
    pygame.image.load("Assets/black_grasshopper.png"), (44, 24)
)
black_beetle = pygame.transform.scale(
    pygame.image.load("Assets/black_beetle.png"), (44, 24)
)

# White pieces
white_ant = pygame.transform.scale(pygame.image.load("Assets/white_ant.png"), (44, 24))
white_spider = pygame.transform.scale(
    pygame.image.load("Assets/white_spider.png"), (44, 24)
)
white_queen = pygame.transform.scale(
    pygame.image.load("Assets/white_queen.png"), (44, 24)
)
white_grasshopper = pygame.transform.scale(
    pygame.image.load("Assets/white_grasshopper.png"), (44, 24)
)
white_beetle = pygame.transform.scale(
    pygame.image.load("Assets/white_beetle.png"), (44, 24)
)


# Hexagon constants

RADIUS = 30
HEX_WIDTH = 2 * RADIUS
