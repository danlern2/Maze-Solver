from __future__ import annotations
from window import Window
from maze import Maze
from tkinter import (
    Tk,
    BOTH,  # type: ignore
    Canvas,  # type: ignore
    ttk,
    dialog,  # type: ignore
    commondialog,  # type: ignore
    Entry,
    Widget,
    StringVar,  # type: ignore
    Label,
    IntVar,
)


class TkMaster(Widget):
    def __init__(self) -> None:
        self.width = 400
        self.height = 200
        self.__root = Tk()
        self.__root.wm_title("Maze Selector")
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.close_button()
        self.text_box()
        self.wait_for_close()

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
        close_button.grid(row=3, column=1)

    def text_box(self):
        text_1_var = IntVar()
        text_2_var = IntVar()
        text_1 = Label(
            self.__root, text="Number of Collumns", font=("calibre", 10, "bold")
        )
        text_1_entry = Entry(
            self.__root, textvariable=text_1_var, font=("calibre", 10, "normal")
        )
        text_2 = Label(self.__root, text="Number of Rows", font=("calibre", 10, "bold"))
        text_2_entry = Entry(
            self.__root, textvariable=text_2_var, font=("calibre", 10, "normal")
        )

        text_1.grid(row=0, column=0)
        text_1_entry.grid(row=0, column=1)
        text_2.grid(row=1, column=0)
        text_2_entry.grid(row=1, column=1)

        def submit():
            text_1_val = text_1_var.get()
            text_2_val = text_2_var.get()
            if text_1_val > 30:
                return "Too many collumns"
            if text_2_val > 30:
                return "Too many rows"
            # print(text_1_val)
            # self.bind()
            self.maze_run(text_1_val, text_2_val)
            return

        sub_btn = ttk.Button(self.__root, text="Submit", command=submit)
        sub_btn.grid(row=1, column=1)

    def maze_run(self, text_1_val: int, text_2_val: int):
        program = maze_creator(text_1_val, text_2_val, 40, 40)
        win = program[0]
        maze = program[1]
        maze.break_walls()
        maze.solve()
        win.wait_for_close()
        return win


def maze_creator(
    num_col: int,
    num_row: int,
    cell_size_x: int,
    cell_size_y: int,
    seed=None,  # type: ignore
) -> tuple[Window, Maze]:
    win_x = num_col * cell_size_x + 10
    win_y = num_row * cell_size_y + 10
    win = Window(win_x, win_y)
    maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, win, seed)  # type: ignore
    return win, maze


def test():
    master = TkMaster()  # type: ignore
    # entry = Entry(master, str)


test()
