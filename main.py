import pygame
import sys
import random


from hive.ui.menu import HiveMenu
from hive.ui.gameover import HiveGameOver
from hive.game import HiveGame
# import cProfile
# import pstats


def main():
    """
    Main entry point for the Hive game
    """
    pygame.display.set_caption("Hive")

    # Get game configuration
    while True:
        # Create menu
        menu = HiveMenu()
        game_config = menu.main_menu()

        # If user quits from menu
        if game_config is None:
            break

        # Create and start the game
        game = HiveGame(game_config)
        end_game_result = game.run_game()
        if not end_game_result:
            break
        game_over = HiveGameOver()
        game_over.show_endgame_screen(end_game_result)
        return_to_menu = game_over.handle_endgame_input()
        if not return_to_menu:
            break

    # Quit pygame
    pygame.quit()


if __name__ == "__main__":
    # profiler = cProfile.Profile()
    # profiler.enable()
    random.seed(10) # set random seed
    main()
    # profiler.disable()
    # stats = pstats.Stats(profiler)
    # stats.sort_stats("cumtime")  # Sort by cumulative time
    # stats.print_stats(10000)  # Print top 20 time-consuming functions
