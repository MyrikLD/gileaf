from tkinter import Canvas
from typing import TYPE_CHECKING

from enums import ConnState
from static import CONNECT_TRASHOLD

if TYPE_CHECKING:
    from .socket import Socket


class SocketPair:
    def __init__(self, *args: "Socket"):
        self.a, self.b = sorted(args, key=lambda s: id(s))

    @property
    def distance(self) -> float:
        return (
            (self.a.x_abs - self.b.x_abs) ** 2 + (self.a.y_abs - self.b.y_abs) ** 2
        ) ** 0.5

    def __repr__(self):
        return f"({self.a}<-{round(self.distance)}->{self.b})"

    def __hash__(self):
        return hash((self.a, self.b))

    def __contains__(self, item: "Socket"):
        return item in (self.a, self.b)

    def __iter__(self):
        yield self.a
        yield self.b


class Neighbor(SocketPair):
    id: int | None = None

    def draw(self, canvas: Canvas):
        self.id = canvas.create_line(
            self.a.x_abs,
            self.a.y_abs,
            self.b.x_abs,
            self.b.y_abs,
            fill="yellow",
        )

    def undraw(self, canvas: Canvas):
        if self.id:
            canvas.delete(self.id)
            self.id = None

    @property
    def connection(self):
        return Connection(*self)


class Connection(SocketPair):
    def update(self, canvas: Canvas):
        if self.distance < CONNECT_TRASHOLD:
            self.connect(canvas)
        else:
            self.disconnect(canvas)

    def connect(self, canvas: Canvas):
        for s in self:
            if s.state != ConnState.CONNECTED or s.connection != self:
                s.state = ConnState.CONNECTED
                s.connection = self

                s.redraw(canvas)

    def disconnect(self, canvas: Canvas):
        for s in self:
            if s.state != ConnState.EMPTY or s.connection is not None:
                s.state = ConnState.EMPTY
                s.connection = None
                s.redraw(canvas)
