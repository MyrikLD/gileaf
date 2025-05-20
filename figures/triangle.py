import math

from figures.figure import Figure
from utils import is_point_in_triangle


class Triangle(Figure):
    size = 50
    _rotate = 0
    conn_per_side = 1

    @property
    def vertices(self) -> list[tuple[int, int]]:
        r = self.size / math.sqrt(3)

        _vertices = []

        for i in range(3):
            # Angle for each vertex (0°, 120°, 240°)
            # Add 90° so that the first vertex is on top
            angle = math.radians(i * 120 + 90 + self._rotate)
            x = self.x + r * math.cos(angle)
            y = self.y + r * math.sin(angle)
            _vertices.append((round(x), round(y)))

        return _vertices

    def __repr__(self):
        return f"T1({self.x}, {self.y})"
