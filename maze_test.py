from window import Window, Line, Point
from maze import Maze


def maze_creator(
    num_row: int,
    num_col: int,
    cell_size_x: int,
    cell_size_y: int,
    seed=None,  # type: ignore
) -> tuple[Window, Maze]:
    win_x = num_col * cell_size_x + 10
    win_y = num_row * cell_size_y + 10
    win = Window(win_x, win_y)
    maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, win, seed)  # type: ignore
    return win, maze


class TestMaze:
    def test_maze_cell(self):
        num_row = 20
        num_col = 20
        cell_size_x = 20
        cell_size_y = 20
        maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y)

        assert len(maze.cells) == num_col
        assert len(maze.cells[0]) == num_row

    def test_maze_cell_2(self):
        num_row = 50
        num_col = 10
        cell_size_x = 30
        cell_size_y = 10
        maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y)

        assert len(maze.cells) == num_col
        assert len(maze.cells[0]) == num_row

    def test_entrance_and_exit(self):
        num_row = 8
        num_col = 8
        cell_size_x = 20
        cell_size_y = 20
        maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, seed="blep")

        assert maze.cells[0][0].has_top_wall is False
        assert maze.cells[num_col - 1][num_row - 1].has_bottom_wall is False

    def test_visited_reset(self):
        num_row = 8
        num_col = 8
        cell_size_x = 20
        cell_size_y = 20
        maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, seed="blep")
        maze.break_walls()
        maze._reset_cells_visited()  # type: ignore

        assert maze.cells[0][0].visited is False
        assert maze.cells[num_col - 1][num_row - 1].visited is False

    def test_visited_reset2(self):
        num_row = 8
        num_col = 8
        cell_size_x = 20
        cell_size_y = 20
        maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, seed="blep")
        maze.break_walls()
        maze._reset_cells_visited()  # type: ignore

        assert maze.cells[0][0].visited is False
        assert maze.cells[num_col - 1][num_row - 2].visited is False


def basic_window_test():
    win = Window(800, 600)

    win.wait_for_close()


# basic_window_test()


def window_line_test():
    win = Window(800, 600)
    win.draw_line(Line(Point(5, 5), Point(100, 200)), "blue")
    win.wait_for_close()


# window_line_test()


def window_box_test():
    win = Window(800, 600)
    win.draw_line(Line(Point(5, 5), Point(5, 200)), "red")
    win.draw_line(Line(Point(5, 200), Point(200, 200)), "blue")
    win.draw_line(Line(Point(200, 200), Point(200, 5)), "green")
    win.draw_line(Line(Point(200, 5), Point(5, 5)), "yellow")
    win.wait_for_close()


# window_box_test()


def maze_cell_test():
    win = Window(800, 800)
    num_row = 20
    num_col = 20
    cell_size_x = 20
    cell_size_y = 20
    Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, win)

    win.wait_for_close()


# maze_cell_test()


def entrance_and_exit_test():
    win = Window(200, 200)
    num_row = 8
    num_col = 8
    cell_size_x = 20
    cell_size_y = 20
    Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, win)

    win.wait_for_close()


# entrance_and_exit_test()


def test_break_walls():
    win = Window(200, 200)
    num_row = 8
    num_col = 8
    cell_size_x = 20
    cell_size_y = 20
    maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, win, "blep")
    maze.break_walls()
    win.wait_for_close()

    assert maze.cells[1][0].visited is False
    assert maze.cells[num_col - 1][num_row - 2].visited is False


def test_small_break_walls():
    win = Window(200, 200)
    num_row = 3
    num_col = 3
    cell_size_x = 40
    cell_size_y = 40
    maze = Maze(5, 5, num_col, num_row, cell_size_x, cell_size_y, win, "blep")
    maze.break_walls()
    win.wait_for_close()

    assert maze.cells[0][1].visited is False
    assert maze.cells[num_col - 1][num_row - 2].visited is False


def test_solve():
    Program = maze_creator(8, 8, 40, 40, "blep")
    win = Program[0]
    maze = Program[1]
    maze.break_walls()
    maze.solve()
    win.wait_for_close()

    # assert maze.cells[0][0].visited is False
    # assert maze.cells[num_col - 1][num_row - 2].visited is False


# test_solve()


def test_random():
    Program = maze_creator(8, 8, 40, 40)
    win = Program[0]
    maze = Program[1]
    maze.break_walls()
    maze.solve()
    win.wait_for_close()


# test_random()


def test_random_large():
    Program = maze_creator(20, 20, 40, 40)
    win = Program[0]
    maze = Program[1]
    maze.break_walls()
    maze.solve()
    win.wait_for_close()


# test_random_large()
