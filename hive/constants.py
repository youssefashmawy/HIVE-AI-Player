import pygame
from hive.orientation import Orientation
from math import sqrt
from hive.layout import Layout
from hive.point import Point

WIDTH, HEIGHT = 900, 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)


FPS = 15
PIECES_SCALING = (60, 60)


# Images
background_image = pygame.image.load("HIVE-AI-PLAYER/Assets/board_background.jpg")


# Black pieces
black_ant = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/black_ant.png"), PIECES_SCALING
)
black_spider = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/black_spider.png"), PIECES_SCALING
)
black_queen = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/black_queen.png"), PIECES_SCALING
)
black_grasshopper = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/black_grasshopper.png"), PIECES_SCALING
)
black_beetle = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/black_beetle.png"), PIECES_SCALING
)


# White pieces
white_ant = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/white_ant.png"), PIECES_SCALING
)
white_spider = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/white_spider.png"), PIECES_SCALING
)
white_queen = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/white_queen.png"), PIECES_SCALING
)
white_grasshopper = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/white_grasshopper.png"), PIECES_SCALING
)
white_beetle = pygame.transform.scale(
    pygame.image.load("HIVE-AI-PLAYER/Assets/white_beetle.png"), PIECES_SCALING
)


# Hexagon constants

GRID_WIDTH = 6
GRID_HEIGHT = 6
HEX_RADIUS = 30

# Flat top calculation

LAYOUT_FLAT = Orientation(
    (3.0 / 2.0, 0.0, sqrt(3.0) / 2.0, sqrt(3.0)),
    (2.0 / 3.0, 0.0, -1.0 / 3.0, sqrt(3.0) / 3.0),
    0.0,
)

LAYOUT = Layout(
    LAYOUT_FLAT,
    Point(HEX_RADIUS, HEX_RADIUS),
    Point(WIDTH // 2, HEIGHT // 2),
)
