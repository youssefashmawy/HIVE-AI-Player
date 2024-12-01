import pygame


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
        return f"Point({self.q}, {self.r}, {self.s})"
