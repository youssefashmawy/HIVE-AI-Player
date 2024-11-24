# Class Diagrams

```mermaid
classDiagram
    Board: +List[List] board
    Board: +Piece selected_piece
    Board: +int red_left
    Board: +int white_left
    Board: +draw_hexagons()-> None
    Board: +draw()-> None
    Board: +move(Piece, int, int)-> None
    Board: +get_piece(Piece, int, int)-> Piece

    Piece: +int row
    Piece: +int col
    Piece: +int PADDING
    Piece: +int OUTLINE
    Piece: +int color
    Piece: +calc_pos()
    Piece: +draw(img)
    Piece: +move()*

    class SoldierAnt{
        +int count = 3
        +move()
    }    
    class Beetles{
        +int count = 2
        +move()
    }
    class QueenBee{
        +int count = 1
        +int count_neighbours
        +bool is_surrounded
        +move()
    }
    class GrassHoppers{
        +int count = 3
        +move()
    }
        class Spider{
        +int count = 2
        +move()
    }

    Board o-- Piece
    Piece <|-- SoldierAnt
    Piece <|-- Beetles
    Piece <|-- QueenBee
    Piece <|-- GrassHoppers
    Piece <|-- Spider

```
