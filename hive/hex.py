import pygame
import numpy as np


class Hex:
    def __init__(self, q: int, r: int):
        # Axial coordinates
        self.q = q
        self.r = r
        self.s = -q - r

    def __eq__(self, other: "Hex"):
        if not isinstance(other, Hex):
            print("Error in hex.py")
            return NotImplemented
        return (self.q, self.r) == (other.q, other.r)

    def __repr__(self):
        return f"Point({self.q}, {self.r}, {self.s})"
