from __future__ import annotations
import time
import random
from typing import Any
from window import Window, Point
from cell import Cell


class Maze:
    """
    `Maze(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win)`
    The x/y position of the maze represents how many pixels from the top and left the maze should start from the side of the window
    """

    def __init__(
        self,
        x1: int,
        y1: int,
        num_cols: int,
        num_rows: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window | None = None,
        seed: Any | None = None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cells: list[list[Cell]] = []
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            self.seed = random.seed(seed)
            self.__random_seed = True
        else:
            self.seed = seed
            self.__random_seed = False
        self.__create_cells()
        self.__start_end = self._break_entrance_and_exit()
        self.start = self.__start_end[0]
        self.end = self.__start_end[1]

    def __repr__(self) -> str:
        return f"Maze({self.x1}, {self.y1}, {self.num_rows}, {self.num_cols}, {self.cells}, {self.cell_size_x}, {self.cell_size_y}, {self.win})"

    def __create_cells(self):
        # i: int = 0
        # j: int = 0
        for i in range(self.num_cols):
            col: list[Cell] = []
            for j in range(self.num_rows):
                cell: Cell = self.__draw_cell(i, j, init=True)
                col.append(cell)

            self.cells.append(col)
        return

    def __draw_cell(self, i: int, j: int, init: bool = False):
        """
        `i` is the collumn number, `j` is the row number.
        ### When `init` is True, this method will create a new cell at the position on the canvas calculated from `i` and `j`
        - the top left point of each cell is `Point((i * self.cell_size_x + self.x1), (j * self.cell_size_y + self.y1))`
        - the bottom right point of each cell is `Point((top left x + self.cell_size_x), (top left y + self.cell_size_y))
        """
        if init:
            top_left = Point(
                (i * self.cell_size_x + self.x1), (j * self.cell_size_y + self.y1)
            )
            bottom_right = Point(
                (top_left.x + self.cell_size_x), (top_left.y + self.cell_size_y)
            )
            new_cell: Cell = Cell(i, j, self.win, top_left, bottom_right)
            if self.win is None:
                return new_cell
            new_cell.draw()
            self.__animate(0.001)
            return new_cell

        else:
            cell = self.cells[i][j]
            if self.win is None:
                return cell

            cell.draw()
            self.__animate()
            return cell

    def __animate(self, sleep: float = 0.005):
        if self.win is None:
            return

        self.win.redraw()
        time.sleep(sleep)

    def _break_entrance_and_exit(self):
        if self.__random_seed is True:
            start = self.cells[0][0]
            start_index: tuple[int, int] = 0, 0
            start.has_top_wall = False
            self.__draw_cell(0, 0)
            end = self.cells[self.num_cols - 1][self.num_rows - 1]
            end_index = self.num_cols - 1, self.num_rows - 1
            end.has_bottom_wall = False
            self.__draw_cell(self.num_cols - 1, self.num_rows - 1)

        else:
            choices = [0, self.num_rows - 1]
            choice = random.choice(choices)
            rand = random.randrange(0, self.num_cols)
            start = self.cells[rand][choice]
            start_index: tuple[int, int] = rand, choice
            if choice == choices[0]:
                start.has_top_wall = False
                choice = choices[1]
            else:
                start.has_bottom_wall = False
                choice = choices[0]
            self.__draw_cell(rand, choice)

            rand = random.randrange(0, self.num_cols)
            end = self.cells[rand][choice]
            end_index: tuple[int, int] = rand, choice
            if choice == choices[0]:
                end.has_top_wall = False
            else:
                end.has_bottom_wall = False
            self.__draw_cell(rand, choice)
        return start_index, end_index

    def break_walls(self):
        self._break_walls_r()
        self._reset_cells_visited()

    def _break_walls_r(self, i: int = 0, j: int = 0):
        cell = self.cells[i][j]
        cell.visited = True
        while True:
            to_visit: list[tuple[int, int]] = []
            if j < self.num_rows - 1 and self.cells[i][j + 1].visited is False:
                to_visit.append((i, j + 1))
            if j > 0 and self.cells[i][j - 1].visited is False:
                to_visit.append((i, j - 1))
            if i < self.num_cols - 1 and self.cells[i + 1][j].visited is False:
                to_visit.append((i + 1, j))
            if i > 0 and self.cells[i - 1][j].visited is False:
                to_visit.append((i - 1, j))
            if len(to_visit) == 0:
                self.__draw_cell(i, j)
                return
            rand = random.randrange(0, len(to_visit))
            choice = to_visit[rand]
            other_cell: Cell = self.cells[choice[0]][choice[1]]
            if i < choice[0]:
                cell.has_right_wall = False
                other_cell.has_left_wall = False
            if i > choice[0]:
                cell.has_left_wall = False
                other_cell.has_right_wall = False
            if j < choice[1]:
                cell.has_bottom_wall = False
                other_cell.has_top_wall = False
            if j > choice[1]:
                cell.has_top_wall = False
                other_cell.has_bottom_wall = False
            self.__draw_cell(i, j)
            self.__draw_cell(choice[0], choice[1])
            self._break_walls_r(choice[0], choice[1])

    def _reset_cells_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        i: int = self.start[0]
        j: int = self.start[1]
        start: Cell = self.cells[i][j]
        start.draw_start_and_end()
        self.connect_cells(start)
        self._solve_r(start)
        self.cells[self.end[0]][self.end[1]].draw_start_and_end()
        return

    def connect_cells(self, cell: Cell):
        i = cell.pos_col
        j = cell.pos_row
        cell.visited = True
        if (
            j < self.num_rows - 1
            and self.cells[i][j + 1].visited is False
            and self.cells[i][j + 1].has_top_wall is False
        ):
            cell.connected.append(self.cells[i][j + 1])
            self.cells[i][j + 1].parent = cell
            self.connect_cells(self.cells[i][j + 1])
        if (
            j > 0
            and self.cells[i][j - 1].visited is False
            and self.cells[i][j - 1].has_bottom_wall is False
        ):
            cell.connected.append(self.cells[i][j - 1])
            self.cells[i][j - 1].parent = cell
            self.connect_cells(self.cells[i][j - 1])
        if (
            i < self.num_cols - 1
            and self.cells[i + 1][j].visited is False
            and self.cells[i + 1][j].has_left_wall is False
        ):
            cell.connected.append(self.cells[i + 1][j])
            self.cells[i + 1][j].parent = cell
            self.connect_cells(self.cells[i + 1][j])
        if (
            i > 0
            and self.cells[i - 1][j].visited is False
            and self.cells[i - 1][j].has_right_wall is False
        ):
            cell.connected.append(self.cells[i - 1][j])
            self.cells[i - 1][j].parent = cell
            self.connect_cells(self.cells[i - 1][j])

    def _solve_r(self, cell: Cell, path: list[Cell] = []):
        if cell == self.cells[self.start[0]][self.start[1]]:
            path.append(cell)
        if not cell.connected and cell != self.cells[self.end[0]][self.end[1]]:
            return False
        if cell.connected and cell != self.cells[self.end[0]][self.end[1]]:
            for j, child in enumerate(cell.connected):
                cell.draw_move(child, undo=True)
                path.append(child)
                r = self._solve_r(child, path)
                if r is False:
                    path.remove(child)
                    if j == len(cell.connected) - 1:
                        return False
                elif r is True:
                    return True
        if cell == self.cells[self.end[0]][self.end[1]]:
            time.sleep(1.0)
            for i in range(0, len(path) - 1):
                path[i].draw_move(path[i + 1], undo=False)
        return True
