import pygame
from hive.constants import (
    FPS,
    LAYOUT,
    BLUE,
    background_image,
    WIN,
)
from hive.helper import *
from hive.board import Board
from hive.piece import Piece

pygame.init()

pygame.display.set_caption("Hive")
WIN.blit(background_image, (0, 0))


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board(1)
    setup_board(board)
    draw_pieces(board)
    print(board)
    selected_piece = None  # Keep track of the selected piece

    while run:
        clock.tick(FPS)
        WIN.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draw the background and pieces

        # Draw the hex grid
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            hex_clicked = pixel_to_hex(LAYOUT, pos)
            piece = board.select_piece_by_hex(hex_clicked)

            if selected_piece is None:
                # Select a piece
                if piece:
                    selected_piece = piece
                    print(f"Selected piece at {selected_piece.hex}")
                    # Optionally, highlight the selected piece or show possible moves
            else:
                # Try to move the selected piece to the clicked hex
                if board.is_valid_move(selected_piece, hex_clicked):
                    # Check breaking the hive
                    print(board.not_break_hive(selected_piece), end="\n\n")
                    board.move(selected_piece.hex, hex_clicked)
                    print(f"Moved piece to {hex_clicked}")
                    board.remove_piece_by_hex(selected_piece.hex)
                    selected_piece.hex = hex_clicked
                    board.increment_pieces_placed(selected_piece)
                    print(board)
                    selected_piece = None
                else:
                    print("Invalid move. Please select a valid destination.")
                    selected_piece = None  # Deselect the piece
        draw_pieces(board)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

# TODO
# Draw suggested moves using draw_hex
# Add an outline to make hexas look nicer
# Implement sliding algorithm
# Implement not pinned
# Implement immbolized
# Implement AI vs player
# Implement AI vs AI
