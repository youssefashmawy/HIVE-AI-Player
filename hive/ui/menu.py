import pygame
from ..helper import resource_path

class HiveMenu:
    def __init__(self, screen_width=800, screen_height=600):
        pygame.init()

        # Screen setup
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Hive Game Menu")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.HOVER_COLOR = (150, 150, 150)

        # Fonts
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

        self.background = pygame.image.load(resource_path("./Assets/board_background.jpg"))
        self.background = pygame.transform.scale(
            self.background, (screen_width, screen_height)
        )

        # Menu options
        self.menu_options = ["Player vs Player", "AI vs Player", "AI vs AI", "Quit"]

        # AI Difficulty options
        self.ai_difficulties = ["Easy", "Medium", "Hard"]

        # Game state
        self.game_config = {"mode": None, "difficulty_1": None, "difficulty_2": None}

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def main_menu(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill(self.BLACK)

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Draw title
            self.draw_text(
                "Hive Game Menu", self.font, self.WHITE, self.screen_width // 2, 100
            )

            # Draw menu options
            for i, option in enumerate(self.menu_options):
                option_y = 250 + i * 75
                option_rect = pygame.Rect(
                    self.screen_width // 2 - 150, option_y, 300, 50
                )

                # Hover effect
                if option_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(self.screen, self.HOVER_COLOR, option_rect)
                else:
                    pygame.draw.rect(self.screen, self.GRAY, option_rect)

                # Draw option text
                self.draw_text(
                    option,
                    self.small_font,
                    self.BLACK,
                    self.screen_width // 2,
                    option_y + 25,
                )

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, option in enumerate(self.menu_options):
                        option_y = 250 + i * 75
                        option_rect = pygame.Rect(
                            self.screen_width // 2 - 150, option_y, 300, 50
                        )

                        if option_rect.collidepoint(event.pos):
                            if option == "Quit":
                                return None
                            elif option == "Player vs Player":
                                self.game_config["mode"] = "PvP"
                                return self.game_config
                            elif option in ["AI vs Player", "AI vs AI"]:
                                return self.difficulty_menu(option)

            pygame.display.flip()
            clock.tick(30)

        return None

    def difficulty_menu(self, mode):
        clock = pygame.time.Clock()
        running = True
        difficulty_1_selected = None
        difficulty_2_selected = None

        while running:
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill(self.BLACK)

            # Draw title
            self.draw_text(
                f"{mode} Difficulty", self.font, self.WHITE, self.screen_width // 2, 100
            )

            # Draw instructions
            instruction_text = (
                "Select First Difficulty"
                if not difficulty_1_selected
                else "Select Second Difficulty"
            )
            self.draw_text(
                instruction_text,
                self.small_font,
                self.WHITE,
                self.screen_width // 2,
                170,
            )

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Store rectangles for each difficulty
            difficulty_rects = []

            # Draw AI difficulty options
            for i, diff in enumerate(self.ai_difficulties):
                diff_1_y = 250
                diff_1_rect = pygame.Rect(
                    self.screen_width // 2 - 300, diff_1_y + i * 75, 250, 50
                )

                # Second AI difficulty (only if AI vs AI)
                diff_2_rect = pygame.Rect(
                    self.screen_width // 2 + 50, diff_1_y + i * 75, 250, 50
                )

                # Color for first difficulty selection
                if not difficulty_1_selected:
                    if diff_1_rect.collidepoint(mouse_x, mouse_y):
                        pygame.draw.rect(self.screen, self.HOVER_COLOR, diff_1_rect)
                    else:
                        pygame.draw.rect(self.screen, self.GRAY, diff_1_rect)
                else:
                    # First difficulty already selected
                    pygame.draw.rect(self.screen, (100, 100, 100), diff_1_rect)

                # Draw first difficulty text
                self.draw_text(
                    diff,
                    self.small_font,
                    self.BLACK,
                    self.screen_width // 2 - 175,
                    diff_1_y + i * 75 + 25,
                )

                # Store rectangles for event handling
                difficulty_rects.append(
                    {
                        "difficulty": diff,
                        "first_rect": diff_1_rect,
                        "second_rect": diff_2_rect if mode == "AI vs AI" else None,
                    }
                )

                # For AI vs AI mode
                if mode == "AI vs AI":
                    # Color for second difficulty selection
                    if difficulty_1_selected:
                        if diff_2_rect.collidepoint(mouse_x, mouse_y):
                            pygame.draw.rect(self.screen, self.HOVER_COLOR, diff_2_rect)
                        else:
                            pygame.draw.rect(self.screen, self.GRAY, diff_2_rect)
                    else:
                        # Disable second difficulty selection before first is chosen
                        pygame.draw.rect(self.screen, (100, 100, 100), diff_2_rect)

                    self.draw_text(
                        diff,
                        self.small_font,
                        self.BLACK,
                        self.screen_width // 2 + 175,
                        diff_1_y + i * 75 + 25,
                    )

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for diff_info in difficulty_rects:
                        # First difficulty selection
                        if (
                            diff_info["first_rect"].collidepoint(event.pos)
                            and not difficulty_1_selected
                        ):
                            if mode == "AI vs Player":
                                self.game_config["mode"] = mode
                                self.game_config["difficulty_1"] = diff_info[
                                    "difficulty"
                                ]
                                return self.game_config
                            elif mode == "AI vs AI":
                                # Mark first difficulty as selected
                                difficulty_1_selected = diff_info["difficulty"]
                                self.game_config["mode"] = mode
                                self.game_config["difficulty_1"] = diff_info[
                                    "difficulty"
                                ]

                        # Second difficulty selection for AI vs AI
                        if (
                            mode == "AI vs AI"
                            and difficulty_1_selected
                            and diff_info["second_rect"]
                            and diff_info["second_rect"].collidepoint(event.pos)
                        ):
                            difficulty_2_selected = diff_info["difficulty"]
                            self.game_config["difficulty_2"] = diff_info["difficulty"]
                            return self.game_config

            # If first difficulty is selected, show it
            if difficulty_1_selected:
                selected_text = f"First Difficulty: {difficulty_1_selected}"
                self.draw_text(
                    selected_text,
                    self.small_font,
                    self.WHITE,
                    self.screen_width // 2,
                    500,
                )

            pygame.display.flip()
            clock.tick(30)

        return None
