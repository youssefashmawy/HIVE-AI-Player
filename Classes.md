# Class Diagrams

```mermaid
classDiagram
    Board: +List[List] board
    Board: +Piece selected_piece
    Board: +int red_left
    Board: +int white_left
    Board: +draw_hexagons()-> None
    Board: +draw()-> None
    Board: +all_possible_moves(Piece, int, int)-> None
    Board: +get_piece(Piece, int, int)-> Piece

    Piece: +int row
    Piece: +int col
    Piece: +int PADDING
    Piece: +int OUTLINE
    Piece: +int color
    Piece: +calc_pos()
    Piece: +draw(img, x, y)
    Piece: +generate_allowed_placement()
    Piece: +all_possible_moves()*
    Piece: +generate_allowed_all_possible_movess()*

    class SoldierAnt{
        +int count = 3
        +all_possible_moves()
        generate_allowed_all_possible_movess()
    }    
    class Beetles{
        +int count = 2
        +all_possible_moves()
        +generate_allowed_all_possible_movess()
    }
    class QueenBee{
        +int count = 1
        +int count_neighbours
        +bool is_surrounded
        +all_possible_moves()
        +generate_allowed_all_possible_movess()
    }
    class GrassHoppers{
        +int count = 3
        +all_possible_moves()
        +generate_allowed_all_possible_movess()
    }
        class Spider{
        +int count = 2
        +all_possible_moves()
        +generate_allowed_all_possible_movess()
    }

    Board o-- Piece
    Piece <|-- SoldierAnt
    Piece <|-- Beetles
    Piece <|-- QueenBee
    Piece <|-- GrassHoppers
    Piece <|-- Spider

```
