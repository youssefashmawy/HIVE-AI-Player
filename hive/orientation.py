class Orientation:
    """Helps Layout class define orientation of the hexagon"""

    def __init__(
        self,
        f: tuple[float],
        b: tuple[float],
        start_angle=0,
    ):
        self.f = f
        self.b = b
        self.start_angle = start_angle


# layout_flat
#   = Orientation((3.0 / 2.0, 0.0, sqrt(3.0) / 2.0, sqrt(3.0)),
# (2.0 / 3.0, 0.0, -1.0 / 3.0, sqrt(3.0) / 3.0),
# 0.0);
