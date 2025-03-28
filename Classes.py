from tkinter import Tk, BOTH, Canvas
import time
class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill = BOTH, expand = 1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running == True:
            self.redraw()
    def close(self):
        self.__running = False
    def draw_line(self, line, fill_color = "black"):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill = fill_color, width = 2)

class Cell:
    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = window
    
    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2= x2
        self._y2 = y2
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x2, self._y1)
        p3 = Point(self._x1, self._y2)
        p4 = Point(self._x2, self._y2)
        if self.has_left_wall == True:
            left_wall = Line(p1, p3)
            self._win.draw_line(left_wall)
        if self.has_top_wall == True:
            top_wall = Line(p1, p2)
            self._win.draw_line(top_wall)
        if self.has_right_wall == True:
            right_wall = Line(p2, p4)
            self._win.draw_line(right_wall)
        if self.has_bottom_wall == True:
            bottom_wall = Line(p3, p4)
            self._win.draw_line(bottom_wall)
        
    def draw_move(self, to_cell, undo=False):
        p1 = Point((self._x1+self._x2)/2, (self._y1+self._y2)/2)
        p2 = Point((to_cell._x1 + to_cell._x2)/2, (to_cell._y1 + to_cell._y2)/2)
        line = Line(p1, p2)
        color = "grey"
        if undo == True:
            color = "red"
        self._win.draw_line(line, color )

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        
    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            list = []
            for j in range(self._num_rows):
                cell = Cell(self._win)
                list.append(cell)
            self._cells.append(list)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i , j)

    def _draw_cell(self, i, j):
        x1 = i*  self._cell_size_x + self._x1
        y1 = j * self._cell_size_y + self._y1
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(.05)

        

        