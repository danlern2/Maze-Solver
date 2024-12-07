from __future__ import annotations
from tkinter import Tk, BOTH, Canvas, ttk, Widget, Frame, Toplevel  # type: ignore
# from tk_master import TkMaster

# from functools import lru_cache
import time
# import time
# import random
# from typing import Any


class Window(Toplevel):
    def __init__(self, root: Tk, width: int, height: int) -> None:
        # super().__init__(root)
        self.width = width
        self.height = height
        # self._master: Tk = master
        self.__root = root
        # self.__root.wm_title("Maze")
        self.canvas = Canvas(self.__root, bg="gray", height=height, width=width)
        self.canvas.pack(side="top", fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.stop_id = "None"
        # self.close_button()
        self.redraw()
        # self.__root.mainloop()
        # self.wait_for_close()

    # def redraw(self: Window):
    #     if self.__running is True:
    #         self.after(5, self.redraw)
    #     else:
    #         pass

    def redraw(self):
        self.canvas.update_idletasks()
        self.canvas.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running is True:
            self.redraw()

    def close(self):
        self.__running = False
        self.canvas.destroy()
        # self.__root.destroy()

    def close_button(self):
        close_button = ttk.Button(self.__root, text="Close", command=self.close)
        close_button.pack()

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)


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
        try:
            canvas.create_line(
                self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2
            )
        except Exception as e:  # type: ignore
            time.sleep(0.0)

    # def erase(self, canvas: Canvas):
    #     canvas.delete(self)
