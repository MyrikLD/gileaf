import math

from utils import is_point_in_triangle
from .figure import Figure
from .socket import Socket


class Hexagon(Figure):
    size = 86
    conn_per_side = 1
    _rotate = 0

    @property
    def vertices(self) -> list[tuple[int, int]]:
        r = self.size / math.sqrt(3)

        _vertices = []

        for i in range(6):
            # Angle for each vertex (0°, 120°, 240°)
            # Add 90° so that the first vertex is on top
            angle = math.radians(i * 60 + 90 + self._rotate)
            x = self.x + r * math.cos(angle)
            y = self.y + r * math.sin(angle)
            _vertices.append((round(x), round(y)))

        return _vertices
