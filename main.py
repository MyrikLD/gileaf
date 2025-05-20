from tkinter import *

from enums import ConnState, StateEnum
from figures.connection import Connection, Neighbor
from figures.controller import Controller
from figures.figure import Figure
from figures.hexagon import Hexagon
from figures.triangle import Triangle
from figures.triangle_big import BigTriangle
from static import CONNECT_TRASHOLD, MAGNETIC_THRESHOLD

figure_names = {"T1": Triangle, "T2": BigTriangle, "H": Hexagon, "C": Controller}


class LabelTool:
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("LabelTool")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)

        self.figure_select = StringVar(master, "T1")

        # Dictionary to create multiple buttons
        values = {v.__name__: k for k, v in figure_names.items()}

        # Loop is used to create multiple Radiobuttons
        # rather than creating each button separately
        f = Frame(self.frame)
        f.pack(side=TOP, fill=X)
        for text, value in values.items():
            b = Radiobutton(
                f,
                text=text,
                variable=self.figure_select,
                value=value,
            )
            b.pack(side=LEFT)

        # main panel for labeling
        self.canvas = Canvas(self.frame, cursor="tcross")
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<ButtonRelease-1>", self.left_click)

        self.canvas.bind("<Button-2>", self.middle_click)
        # self.canvas.bind("<Button-3>", self.left_click)

        self.canvas.bind("<Button-4>", self.mouse_wheel)
        self.canvas.bind("<Button-5>", self.mouse_wheel)

        self.canvas.bind("<Motion>", self.mouse_move)
        # self.canvas.grid(row=4, column=4, sticky=W + N)
        self.canvas.pack(side=BOTTOM, fill=BOTH, expand=1)

        self.figures: list[Triangle] = []

        self.last_move = None
        self.neibours: list[Neighbor] = []
        self.connections: set[Connection] = set()
        self.parity_creation = False

    def find_figure(self, x, y):
        for i in self.figures[::-1]:
            if i.contains(x, y):
                return i

    def mouse_wheel(self, event: Event):
        direction = {
            4: 1,
            5: -1,
        }[event.num]
        print("wheel", direction)
        f = self.find_figure(event.x, event.y)
        if f:
            f.rotate(self.canvas, direction * 30)
            self.check_connections()

            neibours = self.calc_neibours([f])
            self.update_neibours(neibours)

            self.neibours_to_connections()

    def left_click(self, event: Event):
        f = self.find_figure(event.x, event.y)

        if event.type == EventType.ButtonPress:
            if f:
                f.select(self.canvas, True)
        elif event.type == EventType.ButtonRelease:
            if self.neibours:
                closest_neibours = [
                    i
                    for i in self.neibours
                    if any([i.a.figure.selected, i.b.figure.selected])
                    and not all([i.a.figure.selected, i.b.figure.selected])
                ]
                if (
                    closest_neibours
                    and closest_neibours[0].distance < MAGNETIC_THRESHOLD
                ):
                    neibour = closest_neibours[0]

                    selected = neibour.a if neibour.a.figure.selected else neibour.b
                    unselected = neibour.b if neibour.a.figure.selected else neibour.a

                    move = (
                        selected.x_abs - unselected.x_abs,
                        selected.y_abs - unselected.y_abs,
                    )

                    broken = False
                    for i in filter(lambda f: f.selected, self.figures):
                        for j in filter(lambda f: not f.selected, self.figures):
                            if j.contains(i.x + move[0], i.y + move[1]):
                                broken = True
                                break
                        else:
                            continue
                        break

                    if not broken:
                        for i in filter(lambda f: f.selected, self.figures):
                            i.move(
                                self.canvas,
                                i.x - move[0],
                                i.y - move[1],
                            )

                # neibours -> connections
                self.neibours_to_connections()

            if event.state & StateEnum.Shift:
                return
            for i in self.figures:
                if i.selected:
                    i.select(self.canvas, False)

        if event.type == EventType.ButtonPress:
            self.last_move = event.x, event.y

    def middle_click(self, event: Event):
        f = self.find_figure(event.x, event.y)

        if f:
            for s in f.sockets:
                if s.connection is not None:
                    self.remove_connection(s.connection)
            self.figures.remove(f)
            f.undraw(self.canvas)
        else:
            s = self.figure_select.get()
            cls = figure_names[s]
            f = cls(event.x, event.y, 0 if self.parity_creation else 180)
            self.parity_creation = not self.parity_creation
            f.draw(self.canvas)
            self.figures.append(f)
            for i in self.figures:
                if i.selected:
                    i.select(self.canvas, False)

    def remove_connection(self, c: Connection):
        c.disconnect(self.canvas)
        self.connections.remove(c)

    def check_connections(self):
        for i in list(self.connections):
            if i.distance > CONNECT_TRASHOLD:
                self.remove_connection(i)
            else:
                i.update(self.canvas)

    def update_neibours(self, neibours: list[Neighbor]):
        for i in self.neibours:
            i.undraw(self.canvas)

        for i in neibours:
            i.draw(self.canvas)

        self.neibours = neibours

    def neibours_to_connections(self):
        # neibours -> connections
        for i in self.neibours:
            i.undraw(self.canvas)
            if i.distance < CONNECT_TRASHOLD:
                c = i.connection
                self.connections.add(c)
                c.update(self.canvas)

        self.neibours = []

    def mouse_move(self, event: Event):
        if StateEnum(event.state) & StateEnum.Button1:
            move = (event.x - self.last_move[0], event.y - self.last_move[1])
            selected_figs = [f for f in self.figures if f.selected]

            self.check_connections()
            # print("move", move)
            for i in selected_figs:
                i.move(
                    self.canvas,
                    i.x + move[0],
                    i.y + move[1],
                )

            # neibours
            # neibours = []
            # for figure in selected_figs:
            #     close_figs = sorted(self.figures, key=lambda f: figure.distance(f))[1:7]
            #     # print(figure, close_figs)
            #     conns = [
            #         c
            #         for i in close_figs
            #         for c in i.sockets
            #         if c.state == ConnState.EMPTY
            #     ]
            #
            #     for s in figure.sockets:
            #         neibours.extend(
            #             [
            #                 i
            #                 for i in (
            #                     Neighbor(s, n)
            #                     for n in conns
            #                     if abs(n.angle - s.angle) == 180
            #                 )
            #                 if i.distance < MAGNETIC_THRESHOLD
            #             ]
            #         )

            # self.neibours = sorted(
            #     set(self.neibours),
            #     key=lambda x: x.distance,
            # )
            # for i in self.neibours:
            #     print(i.a.angle - i.b.angle)
            neibours = self.calc_neibours(selected_figs)
            self.update_neibours(neibours)

            self.last_move = event.x, event.y

    def calc_neibours(self, figures: list[Figure]):
        neibours = []
        for figure in figures:
            close_figs = sorted(self.figures, key=lambda f: figure.distance(f))[1:7]

            conns = [
                c for i in close_figs for c in i.sockets if c.state == ConnState.EMPTY
            ]

            for s in figure.sockets:
                neibours.extend(
                    [
                        i
                        for i in (
                            Neighbor(s, n)
                            for n in conns
                            if abs(n.angle - s.angle) == 180
                        )
                        if i.distance < MAGNETIC_THRESHOLD
                    ]
                )
        return neibours


if __name__ == "__main__":
    root = Tk()
    tool = LabelTool(root)
    root.resizable(width=True, height=True)
    root.mainloop()
