import pygame
from hive.constants import Consts  # Replace with your actual constants import


class HiveGameOver:
    def __init__(self):
        self.screen = Consts.WIN

    def show_endgame_screen(self, result: str):
        """
        Display the endgame screen with the result ('white', 'black', or 'draw')
        :param result: The result of the game
        """
        Consts.WIN.blit(Consts.background_image, (0, 0))
        font = pygame.font.Font(None, 74)  # Example font size

        if result == "draw":
            text = "Game Over: Draw!"
        elif result == "white":
            text = "Game Over: White Wins!"
        elif result == "black":
            text = "Game Over: Black Wins!"

        # Render the text
        text_surface = font.render(text, True, Consts.BLACK)
        text_rect = text_surface.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(text_surface, text_rect)

        # Prompt for the next action
        prompt_text = "Press 'Q': Quit, 'M': Menu"
        prompt_text_surface = font.render(prompt_text, True, Consts.BLACK)
        prompt_text_rect = prompt_text_surface.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100)
        )
        self.screen.blit(prompt_text_surface, prompt_text_rect)

        pygame.display.flip()  # Update the display

    def handle_endgame_input(self) -> bool:
        """
        Handle user input after the game ends (whether they want to return to the menu or quit)
        :return: Boolean indicating if the user wants to return to the menu
        """
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Quit the game
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # 'Q' to quit the game
                        return False  # Quit the game
                    elif event.key == pygame.K_m:  # 'M' to return to the main menu
                        return True  # Return to the main menu

        return False  # Default return in case of unexpected input
