import pygame
from .orientation import Orientation
from math import sqrt
from hive.layout import Layout
from hive.point import Point
from .helper import resource_path


class Consts:
    WIDTH, HEIGHT = 900, 750

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)

    FPS = 10
    PIECES_SCALING = (63, 63)

    # Images
    background_image = pygame.image.load(resource_path("Assets/board_background.jpg"))

    # Black pieces
    black_ant = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/black_ant.png")), PIECES_SCALING
    )
    black_spider = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/black_spider.png")), PIECES_SCALING
    )
    black_queen = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/black_queen.png")), PIECES_SCALING
    )
    black_grasshopper = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/black_grasshopper.png")), PIECES_SCALING
    )
    black_beetle = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/black_beetle.png")), PIECES_SCALING
    )

    # White pieces
    white_ant = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/white_ant.png")), PIECES_SCALING
    )
    white_spider = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/white_spider.png")), PIECES_SCALING
    )
    white_queen = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/white_queen.png")), PIECES_SCALING
    )
    white_grasshopper = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/white_grasshopper.png")), PIECES_SCALING
    )
    white_beetle = pygame.transform.scale(
        pygame.image.load(resource_path("Assets/white_beetle.png")), PIECES_SCALING
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
        Point(0, -HEIGHT // 16),
    )

    ITEM_SIZE = 50
    BOARD_SIZE = (800, 500)
    BOARD_POS = (0, 0)
    INVENTORY_HEIGHT = 100

    LOGO_SCALING = (INVENTORY_HEIGHT - 20, INVENTORY_HEIGHT - 20)
    logo_image = pygame.transform.scale(
        pygame.image.load(resource_path("./Assets/logo.png")), LOGO_SCALING
    )
