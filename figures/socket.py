import math
from tkinter import Canvas
from typing import TYPE_CHECKING

from enums import ConnState

if TYPE_CHECKING:
    from .connection import Connection


class Socket:
    id = None
    size = 2
    state = ConnState.EMPTY
    connection: "Connection | None" = None

    def __init__(self, figure, x, y, angle):
        self.figure = figure
        self.x = x
        self.y = y
        self.angle = angle

    def redraw(self, canvas: Canvas):
        self.undraw(canvas)
        self.draw(canvas)

    def draw(self, canvas: Canvas):
        color = {
            ConnState.EMPTY: "#777",
            ConnState.CONNECTED: "#0F0",
            ConnState.POWERED: "#00F",
        }[self.state]
        self.id = canvas.create_oval(
            self.x_abs - self.size,
            self.y_abs - self.size,
            self.x_abs + self.size,
            self.y_abs + self.size,
            width=1,
            outline="gray",
            fill=color,
        )

    def undraw(self, canvas: Canvas):
        if self.id:
            canvas.delete(self.id)
            self.id = None

    @property
    def x_abs(self):
        return self.figure.x + self.x

    @property
    def y_abs(self):
        return self.figure.y + self.y

    def distance(self, other: "Socket"):
        return (
            (self.x_abs - other.x_abs) ** 2 + (self.y_abs - other.y_abs) ** 2
        ) ** 0.5

    def __repr__(self):
        return f"C({self.figure})"
