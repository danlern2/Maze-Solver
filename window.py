from __future__ import annotations
from tkinter import Tk, BOTH, Canvas, ttk
# import time
# import random
# from typing import Any


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.wm_title("Maze")
        self.__canvas = Canvas(self.__root, bg="gray", height=height, width=width)
        self.__canvas.pack(side="top", fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.close_button()

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running is True:
            self.redraw()

    def close(self):
        self.__running = False
        self.__root.destroy()

    def close_button(self):
        close_button = ttk.Button(self.__root, text="Close", command=self.close)
        close_button.pack()

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_1: Point, point_2: Point) -> None:
        self.point_1 = point_1
        self.point_2 = point_2
        self.x1: int = self.point_1.x
        self.y1: int = self.point_1.y
        self.x2: int = self.point_2.x
        self.y2: int = self.point_2.y

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2)

    # def erase(self, canvas: Canvas):
    #     canvas.delete(self)
