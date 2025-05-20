from tkinter import Canvas
from typing import Iterable

from enums import ConnState
from utils import angle, is_point_in_triangle
from .socket import Socket


class Figure:
    id: int | None = None
    conn_per_side: int
    _selected: bool = False
    size: int
    _rotate = 0

    def __init__(self, x: int, y: int, rotate: int = 0):
        self.x = x
        self.y = y
        self._rotate = rotate

        self.sockets = [Socket(self, x, y, a) for x, y, a in self.conn_pos]

    def distance(self, other: "Figure"):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def undraw(self, canvas: Canvas):
        if self.id:
            canvas.delete(self.id)
            self.id = None

            for i in self.sockets:
                i.undraw(canvas)

    def redraw(self, canvas: Canvas):
        self.undraw(canvas)
        self.draw(canvas)

    @property
    def vertices(self) -> list[tuple[int, int]]:
        raise NotImplementedError

    @property
    def conn_pos(self) -> Iterable[tuple[int, int, int]]:
        sides = self.vertices
        for p1, p2 in list(zip(sides, sides[1:] + sides[:-1])):
            mid = p1[0] + (p2[0] - p1[0]) / 2, p1[1] + (p2[1] - p1[1]) / 2
            a = angle(mid[0] - self.x, mid[1] - self.y)

            if self.conn_per_side == 1:
                yield mid[0] - self.x, mid[1] - self.y, a
            elif self.conn_per_side == 2:
                for i in (1, 3):
                    fraction = i / (3 + 1)

                    x = p1[0] + (p2[0] - p1[0]) * fraction
                    y = p1[1] + (p2[1] - p1[1]) * fraction

                    yield x - self.x, y - self.y, a
            else:
                raise NotImplementedError

            # for n in range(1, self.conn_per_side + 1):
            #     fraction = n / (self.conn_per_side + 1)
            #
            #     x = p1[0] + (p2[0] - p1[0]) * fraction
            #     y = p1[1] + (p2[1] - p1[1]) * fraction
            #
            #     yield x - self.x, y - self.y

    def move(self, canvas: Canvas, x: int, y: int):
        self.x = x
        self.y = y
        self.redraw(canvas)

    @property
    def selected(self):
        return self._selected

    def select(self, canvas: Canvas, value: bool):
        self._selected = value
        self.redraw(canvas)

    def rotate(self, canvas: Canvas, angle: float):
        self.undraw(canvas)
        self._rotate = (self._rotate + angle) % 360
        for (x, y, a), connecion in zip(self.conn_pos, self.sockets):
            connecion.x = x
            connecion.y = y
            connecion.angle = a
        self.redraw(canvas)

    def draw(self, canvas: Canvas):
        pos = []
        for i in self.vertices:
            pos.append(canvas.canvasx(i[0]))
            pos.append(canvas.canvasy(i[1]))

        self.id = canvas.create_polygon(
            *pos,
            width=1,
            outline="gray" if not self._selected else "black",
            fill="white",
        )

        for i in self.sockets:
            i.draw(canvas)

    def contains(self, x: float, y: float) -> bool:
        vertices = self.vertices

        for (x1, y1), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1]):
            # for i in range(6):
            # x1, y1 = vertices[i]
            # x2, y2 = vertices[(i + 1) % 6]
            if is_point_in_triangle((x, y), [(self.x, self.y), (x1, y1), (x2, y2)]):
                return True

        return False

    @property
    def powered(self):
        return any(i.state == ConnState.POWERED for i in self.sockets)
