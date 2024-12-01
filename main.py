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
    selected_piece = None  # Keep track of the selected placed piece
    selected_piece_key = None  # Keep track of the selected unplaced piece

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                hex_clicked = pixel_to_hex(LAYOUT, pos)

                if selected_piece_key is None and selected_piece is None:
                    # No piece is currently selected
                    # First, check if clicking on an unplaced piece
                    for key, data in board.unplaced_pieces.items():
                        if data["position"] == hex_clicked and data["count"] > 0:
                            selected_piece_key = key
                            if not board.is_first_move:
                                draw_suggested_moves(
                                    board.get_legal_placements(str(key).split("_")[0])
                                )
                            print(f"Selected unplaced piece: {selected_piece_key}")
                            break
                    else:
                        # Not clicking on an unplaced piece, check if clicking on a placed piece
                        piece = board.select_piece_by_hex(hex_clicked)
                        if piece:
                            selected_piece = piece
                            print(f"Selected placed piece at {selected_piece.hex}")

                    # This is where we draw our suggested moves
                    if board.is_first_move:
                        draw_suggested_moves([Hex(q=0, r=0)])
                    elif board.is_second_move:
                        adj_hex = (
                            Piece(Hex(0, 0), "", "white").generate_adj_hexs().values()
                        )
                        draw_suggested_moves(adj_hex)
                else:
                    # A piece is already selected
                    target_hex = hex_clicked  # The hex where the user clicked
                    if board.is_first_move == False:
                        board.is_second_move = False

                    board.is_first_move = False
                    if selected_piece_key:
                        board.place_piece(target_hex, selected_piece_key)
                        selected_piece_key = None  # Reset selection
                        selected_piece = None
                    elif selected_piece:
                        # Attempt to move the selected placed piece to the clicked hex
                        if board.is_valid_move(selected_piece, target_hex):
                            # Move the piece
                            old_hex = selected_piece.hex
                            print("\n\n")
                            print(board.not_break_hive(selected_piece))
                            board.move(old_hex, target_hex)
                            print(f"Moved piece to {target_hex}")
                            selected_piece = None  # Reset selection
                        else:
                            print("Invalid move. Please select a valid destination.")
                            selected_piece = None  # Reset selection
                    # We only draw our background after we draw a piece
                    WIN.blit(background_image, (0, 0))

                print(board)

        # Redraw the board and pieces
        draw_pieces(board)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

# TODO
# State diagram
# Draw suggested moves using draw_hex(Pieces inside the board) --> DONE
# Draw suggested placements using draw_hex(Pieces outside the board)
# Implement sliding algorithm
# Implement not pinned(Beetle)
# Implement immbolized
# Implement AI vs player
# Implement AI vs AI
# Probably will make board list of stacks to take beetle into consideration
