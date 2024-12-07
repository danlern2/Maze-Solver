from __future__ import annotations
import time
import random  # type: ignore
from typing import Any  # type: ignore
from window import Window, Point, Line


class Cell:
    def __init__(
        self,
        pos_col: int,
        pos_row: int,
        window: Window | None = None,
        top_left_point: Point = Point(),
        bottom_right_point: Point = Point(),
        has_left: bool = True,
        has_right: bool = True,
        has_top: bool = True,
        has_bottom: bool = True,
        visited: bool = False,
    ) -> None:
        self.pos_col = pos_col
        self.pos_row = pos_row
        self.top_left = top_left_point
        self.bottom_right = bottom_right_point
        self._x1 = top_left_point.x
        self._y1 = top_left_point.y
        self._x2 = bottom_right_point.x
        self._y2 = bottom_right_point.y
        self.has_left_wall = has_left
        self.has_right_wall = has_right
        self.has_top_wall = has_top
        self.has_bottom_wall = has_bottom
        self.__left_wall = Line(
            Point(self._x1, self._y1), Point(self._x1, self._y2)
        )  # * x1, only y changes
        self.__right_wall = Line(
            Point(self._x2, self._y1), Point(self._x2, self._y2)
        )  # * x2, only y changes
        self.__top_wall = Line(
            Point(self._x1, self._y1), Point(self._x2, self._y1)
        )  # * y1, only x changes
        self.__bottom_wall = Line(
            Point(self._x1, self._y2), Point(self._x2, self._y2)
        )  # * y2, only x changes
        self.__win = window
        self.visited = visited
        self.connected: list[Cell] = []
        self.parent: Cell | None = None

    def draw(self):
        if self.__win is None:
            return
        if self.has_left_wall:
            self.__win.draw_line(self.__left_wall, "black")
        if self.has_right_wall:
            self.__win.draw_line(self.__right_wall, "black")
        if self.has_top_wall:
            self.__win.draw_line(self.__top_wall, "black")
        if self.has_bottom_wall:
            self.__win.draw_line(self.__bottom_wall, "black")

        if not self.has_left_wall:
            self.__win.draw_line(self.__left_wall, "gray")
        if not self.has_right_wall:
            self.__win.draw_line(self.__right_wall, "gray")
        if not self.has_top_wall:
            self.__win.draw_line(self.__top_wall, "gray")
        if not self.has_bottom_wall:
            self.__win.draw_line(self.__bottom_wall, "gray")

    def draw_move(self, to_cell: Cell, undo: bool = False):
        self_center_x = (self._x2 - self._x1) // 2 + self._x1
        self_center_y = (self._y2 - self._y1) // 2 + self._y1
        self_center = Point(self_center_x, self_center_y)

        to_cell_center_x = (to_cell._x2 - to_cell._x1) // 2 + to_cell._x1
        to_cell_center_y = (to_cell._y2 - to_cell._y1) // 2 + to_cell._y1
        to_cell_center = Point(to_cell_center_x, to_cell_center_y)

        color = "#AB4B28"  # * red
        if undo is False:
            color = "#51DF0D"  # * green
        if self.__win is None:
            return
        move = Line(self_center, to_cell_center)
        self.__win.draw_line(move, color)
        self.__animate(0.01)

    def __animate(self, sleep: float = 0.0005):
        if self.__win is None:
            return

        self.__win.redraw()
        time.sleep(sleep)

    def draw_start_and_end(self):
        self_center_x = (self._x2 - self._x1) // 2 + self._x1
        self_center_y = (self._y2 - self._y1) // 2 + self._y1
        self_center = Point(self_center_x, self_center_y)
        color = "gray"
        point = Point(0, 0)
        if self.has_top_wall is False and self._y1 < 11:
            if not self.parent:
                color = "blue"
            else:
                color = "yellow"
            point = Point((self._x2 - self._x1) // 2 + self._x1, self._y1)

        elif self.has_bottom_wall is False and self._y1 > 10:
            if not self.parent:
                color = "blue"
            else:
                color = "yellow"
            point = Point((self._x2 - self._x1) // 2 + self._x1, self._y2)

        if self.__win is None:
            return

        move = Line(point, self_center)
        self.__win.draw_line(move, color)
        self.__animate()
