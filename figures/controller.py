import math

from figures.figure import Figure
from utils import is_point_in_triangle


class Controller(Figure):
    size = 50
    _rotate = 0
    conn_per_side = 1

    @property
    def vertices(self) -> list[tuple[int, int]]:
        _vertices = []

        # Base dimensions
        width = self.size  # Full width
        height = self.size / 2  # Half height

        # Calculate vertices based on rotation
        angle = math.radians(self._rotate)

        # Create base rectangle vertices (clockwise from top-left)
        base_vertices = [
            (-width / 2, -height / 4),  # Top left
            (width / 2, -height / 4),  # Top right
            (width / 3, height / 2),  # Bottom right
            (-width / 3, height / 2),  # Bottom left
        ]

        # Rotate and translate each vertex
        for base_x, base_y in base_vertices:
            # Rotate point
            rotated_x = base_x * math.cos(angle) - base_y * math.sin(angle)
            rotated_y = base_x * math.sin(angle) + base_y * math.cos(angle)

            # Translate to center position
            x = self.x + rotated_x
            y = self.y + rotated_y

            _vertices.append((round(x), round(y)))

        return _vertices

    @property
    def conn_pos(self):
        yield next(super().conn_pos)

    def __repr__(self):
        return f"T1({self.x}, {self.y})"
