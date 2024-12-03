import pygame
from hive.constants import Consts


class Item:
    def __init__(self, type: str, name: str, count: int, image: pygame.Surface):
        self.type = type
        self.name = name
        self.count = count
        self.image = image
        self.rect = None
        self.selected = False  # Track whether this item is selected

    def __deepcopy__(self, memo: "dict"):
        # create a copy with self.linked_to *not copied*, just referenced.
        return Item(self.type, self.name, self.count, None)

    def set_position(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, Consts.ITEM_SIZE, Consts.ITEM_SIZE)

    def draw(self, screen: pygame.Surface):
        if self.rect:
            # Draw a highlight if selected
            if self.selected:
                pygame.draw.rect(screen, Consts.RED, self.rect.inflate(4, 4), 3)
            # Draw item box

            if self.image:
                screen.blit(
                    pygame.transform.scale(
                        self.image, (Consts.ITEM_SIZE, Consts.ITEM_SIZE)
                    ),
                    self.rect,
                )
            count_text = pygame.font.Font(None, 24).render(
                f"x{self.count}", True, Consts.BLACK
            )
            screen.blit(
                count_text,
                (
                    self.rect.x + Consts.ITEM_SIZE / 2 - 10,
                    self.rect.y + 10 + Consts.ITEM_SIZE,
                ),
            )


class Inventory:
    def __init__(self, x: int, y: int, role: str):
        self.x = x
        self.y = y
        self.items: list[Item] = []
        self.role = role

    def add_item(self, item: Item):
        self.items.append(item)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen, Consts.BLACK, (self.x, self.y, 320, Consts.INVENTORY_HEIGHT), 2
        )
        for i, item in enumerate(self.items):
            item.set_position(self.x + 10 + i * (Consts.ITEM_SIZE + 10), self.y + 10)
            item.draw(screen)

    def handle_click(self, pos: tuple[int, int]) -> Item:
        for item in self.items:
            if item.rect and item.rect.collidepoint(pos) and item.count > 0:
                return item
        return None

    def select(self, selected_item: Item):
        for item in self.items:
            if item.type == selected_item.type and item.name == selected_item.name:
                item.selected = True

    def reset_selected(self):
        for item in self.items:
            if item.rect and item.selected:
                item.selected = False

    def get_item_by_name(self, name: str):
        for item in self.items:
            if item.name == name:
                return item
        return None
