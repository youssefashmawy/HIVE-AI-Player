

class Hex:
    def __init__(self, q: int, r: int):
        # Axial coordinates
        self.q = q
        self.r = r
        self.s = -q - r
        

    def __eq__(self, other: "Hex"):
        return (self.q, self.r) == (other.q, other.r)

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    def __repr__(self):
        return f"Hex({self.q}, {self.r}, {self.s})"
    
    def __add__(self, other: "Hex") -> "Hex":
        if not isinstance(other, Hex):
            print("Error in hex.py")
            return NotImplemented
        return Hex(self.q + other.q, self.r + other.r)

    def __sub__(self, other: "Hex"):
        if not isinstance(other, Hex):
            print("Error in hex.py")
            return NotImplemented
        return Hex(self.q - other.q, self.r - other.r)
    
    def generate_adj_hexs(self) -> list["Hex"]:
        return [self+dir for dir in self.generate_directions()]
    
    def generate_directions(self)-> list["Hex"]:
        return DIRECTIONS
    
    def distance(self, other: "Hex") -> int:
        """
        Calculate the hexagonal distance between this hex and another hex.
        
        :param other: Another hex object
        :return: The hexagonal distance as an integer
        """
        return max(abs(self.q - other.q), abs(self.r - other.r), abs(self.s - other.s))
    

DIRECTIONS = [
    Hex(0,-1),
    Hex(1,-1),
    Hex(1, 0),
    Hex(0,1),
    Hex(-1,1),
    Hex(-1, 0),
]