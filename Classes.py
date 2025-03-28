from tkinter import Tk, BOTH, Canvas
import time
import random
import sys
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
    def __init__(self, window = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = window
        self.visited = False
    
    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2= x2
        self._y2 = y2
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x2, self._y1)
        p3 = Point(self._x1, self._y2)
        p4 = Point(self._x2, self._y2)
        
        left_wall = Line(p1, p3)
        if self.has_left_wall == True:
            self._win.draw_line(left_wall)
        else:
            self._win.draw_line(left_wall, "white")

        
        top_wall = Line(p1, p2)
        if self.has_top_wall == True:
            self._win.draw_line(top_wall)
        else:
            self._win.draw_line(top_wall, "white")

        
        right_wall = Line(p2, p4)
        if self.has_right_wall == True:
            self._win.draw_line(right_wall)
        else:
            self._win.draw_line(right_wall, "white")

        
        bottom_wall = Line(p3, p4)
        if self.has_bottom_wall == True:
            self._win.draw_line(bottom_wall)
        else:
            self._win.draw_line(bottom_wall, "white")
        
    def draw_move(self, to_cell, undo=False):
        p1 = Point((self._x1+self._x2)/2, (self._y1+self._y2)/2)
        p2 = Point((to_cell._x1 + to_cell._x2)/2, (to_cell._y1 + to_cell._y2)/2)
        line = Line(p1, p2)
        color = "grey"
        if undo == True:
            color = "red"
        self._win.draw_line(line, color )

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self.seed = seed
        if seed == None:
            self.seed = random.seed(seed)
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()
        self.solve()
        
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
        if self._win is None:
            return
        x1 = i*  self._cell_size_x + self._x1
        y1 = j * self._cell_size_y + self._y1
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        #time.sleep(.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)

    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True
        while True:
            to_visit = []
            up = None
            right = None
            down = None
            left = None
            
            if i > 0 :
                left = self._cells[i-1][j]
                if left.visited == False and left not in to_visit:
                    to_visit.append(left)
            if j > 0:
                up = self._cells[i][j-1]
                if up.visited == False and up not in to_visit:
                    to_visit.append(up)
            if i < self._num_cols - 1:
                right = self._cells[i+1][j]
                if right.visited == False and right not in to_visit:
                    to_visit.append(right)
            if j < self._num_rows - 1:
                down = self._cells[i][j+1]
                if down.visited == False and down not in to_visit:
                    to_visit.append(down)
            if to_visit == []:
                self._draw_cell(i,j)
                return
            
            destination = to_visit[random.randint(0,len(to_visit)-1)]
            
            if destination == left:
                current.has_left_wall = False
                left.has_right_wall = False
                self._break_walls_r(i-1, j )
            if destination == right:
                current.has_right_wall = False
                right.has_left_wall = False
                self._break_walls_r( i+1, j)
            if destination == up:
                current.has_top_wall = False
                up.has_bottom_wall = False
                self._break_walls_r( i, j-1)
            if destination == down:
                current.has_bottom_wall = False
                down.has_top_wall = False
                self._break_walls_r(i, j+1)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False
    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self, i, j):
        self._animate()
        current = self._cells[i][j]
        current.visited = True
        if current == self._cells[self._num_cols-1][self._num_rows-1]:
            return True
        if i > 0 :
            left = self._cells[i-1][j]
            if left.visited == False and current.has_left_wall == False:
                current.draw_move(left)
                if self._solve_r(i-1, j) == True:
                    return True
                current.draw_move(left, True)

        if j > 0:
            up = self._cells[i][j-1]
            if up.visited == False and current.has_top_wall == False:
                current.draw_move(up)
                if self._solve_r(i, j-1) == True:
                    return True
                current.draw_move(up, True)

        if i < self._num_cols - 1:
            right = self._cells[i+1][j]
            if right.visited == False and current.has_right_wall == False:
                current.draw_move(right)
                if self._solve_r(i+1, j) == True:
                    return True
                current.draw_move(right, True)
                
        if j < self._num_rows - 1:
            down = self._cells[i][j+1]
            if down.visited == False and current.has_bottom_wall == False:
                current.draw_move(down)
                if self._solve_r(i, j+1) == True:
                    return True
                current.draw_move(down, True)
        return False
        






        

        