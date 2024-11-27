# Class Diagrams

```mermaid
classDiagram
    class Board {
        -list~Piece~ board
        -Hex selected_piece
        -int black_pieces_placed
        -int white_pieces_placed
        -int difficulty

        +Board(difficulty: int, selected_piece: Hex)
        +set_selected_piece(selected_piece: Hex): void
        +increment_pieces_placed(piece: Piece): void
        +__repr__(): str
        +remove_piece_by_hex(hex: Hex): Piece | None
        +select_piece_by_hex(hex: Hex): Piece | None
        +is_valid_move(piece: Piece, to_hex: Hex): bool
        +move(from_hex: Hex, to_hex: Hex): void
        +turn(): bool
    }


    class Orientation{
        +int f
        +int b
        +int start_angle = 0
        def Orientation(f:tuple[float] , b:tuple[float], start_angle:int =0) 
    }

    class Piece {
        +Hex hex
        +str piece_name
        +str piece_type
        +Piece(hex: Hex, piece_name: str, piece_type: str)
        +__repr__(): str
        +get_legal_moves_piece()*: List~Piece~
    }
    

    class Hex {
        -int q
        -int r
        -int s

        +Hex(q: int, r: int)
        +__eq__(other: Hex): bool
        +__repr__(): str
    }


    class Layout{
        +Orientation orientation,
        +Point size,
        +Point origin
        +__init__(orientation: Orientation,size: Point,origin: Point = Point(0, 0))
    }


    class Point {
        +int x
        +int y
        +Point(x: int, y: int)
        +__add__(other: Point): Point
        +__sub__(other: Point): Point
        +__repr__(): str
        +round(): Point
    }

    class SoldierAnt{
        +int count = 3
        +SoldierAnt(diffculty:int,...)
        +get_legal_moves_piece()
    }    
    class Beetles{
        +int count = 2
        +Beetles(diffculty:int,...)
        +get_legal_moves_piece()
    }
    class QueenBee{
        +int count = 1
        +int count_neighbours
        +bool is_surrounded
        +QueenBee(diffculty:int,...)
        +get_legal_moves_piece()
    }
    class GrassHoppers{
        +int count = 3
        +GrassHoppers(diffculty:int,...)
        +get_legal_moves_piece()
    }
    class Spider{
        +int count = 2
        +Spider(diffculty:int,...)
        +get_legal_moves_piece()
    }

    Hex <|-- Piece

    Layout o-- Point
    Layout o-- Orientation
    Board o-- Hex
    Piece <|-- SoldierAnt
    Piece <|-- Beetles
    Piece <|-- QueenBee
    Piece <|-- GrassHoppers
    Piece <|-- Spider

```
