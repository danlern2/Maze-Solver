from window import Window, Line, Point
from maze import Cell, Maze


def maze_creator(
    num_row: int, num_col: int, cell_size_x: int, cell_size_y: int, seed=None
) -> tuple[Window, Maze]:
    win_x = num_col * cell_size_x + 10
    win_y = num_row * cell_size_y + 10
    win = Window(win_x, win_y)
    maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, win, seed)
    return win, maze


def main():
    win = Window(800, 600)
    win.draw_line(Line(Point(5, 5), Point(100, 200)), "red")
    win.wait_for_close()


main()
