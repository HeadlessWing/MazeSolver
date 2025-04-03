from tkinter import Tk, BOTH, Canvas, Frame, Label, Entry
import tkinter as tk
import time
import random
import sys
from constants import color_selector
class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.toggle_size_entries = False
        self.control_frame = Frame(self.__root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        self.param_frame = Frame(self.control_frame)
        self.param_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.start_button = tk.Button(self.param_frame, text="Start", command=self.maze_creation)
        self.start_button.grid(row=0, column=6, padx=5, pady=5)

        self.solve_button = tk.Button(self.param_frame, text="Solve", command=self.start_maze_solve)
        self.solve_button.grid(row=0, column=7, padx=5, pady=5)
        
        # Row x Column inputs
        Label(self.param_frame, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        self.rows_entry = Entry(self.param_frame, width=5)
        self.rows_entry.grid(row=0, column=1, padx=5, pady=5)
        self.rows_entry.insert(0, "50")  # Default value
        
        Label(self.param_frame, text="Columns:").grid(row=0, column=2, padx=5, pady=5)
        self.cols_entry = Entry(self.param_frame, width=5)
        self.cols_entry.grid(row=0, column=3, padx=5, pady=5)
        self.cols_entry.insert(0, "100")  # Default value
        
        # Cell size input
        Label(self.param_frame, text="Cell Size:").grid(row=0, column=4, padx=5, pady=5)
        self.cell_size_entry = Entry(self.param_frame, width=5)
        self.cell_size_entry.grid(row=0, column=5, padx=5, pady=5)
        self.cell_size_entry.insert(0, "10")  # Default value
        # Fill window checkbox
        self.fill_window_var = tk.BooleanVar()  # Variable to hold the checkbox state
        self.fill_window_var.set(False)  # Default to not filling

        self.fill_window_check = tk.Checkbutton(
        self.param_frame, 
        text="Fill Window", 
        variable=self.fill_window_var,
    )
        self.fill_window_check.grid(row=1, column=0, columnspan=2, padx=5, pady=1)

        #Animation checkbox: When checked changes funtion to only redraw once after all changes are made
        self.animation_var = tk.BooleanVar()
        self.animation_var.set(True)
        self.animation_check = tk.Checkbutton(
            self.param_frame, 
            text= "Animation", 
            variable=self.animation_var
        )
        self.animation_check.grid(row=1, column=2,columnspan=2, padx=5, pady=1)

        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill = BOTH, expand = 1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.maze = None
    
    def maze_creation(self):
        self.__canvas.delete("all")
        
        
        border = 2
        columns = int(self.cols_entry.get())
        rows = int(self.rows_entry.get())
        cell_size = int(self.cell_size_entry.get())
        if self.fill_window_var.get():
            # Get canvas dimensions
            canvas_width = self.__canvas.winfo_width()-4
            canvas_height = self.__canvas.winfo_height()-4
            
            
            columns = canvas_width // cell_size
            rows = canvas_height // cell_size
            self.cols_entry.delete(0, tk.END)
            self.cols_entry.insert(0, str(columns))
            self.rows_entry.delete(0, tk.END)
            self.rows_entry.insert(0, str(rows))
        
        self.maze = Maze(border,  rows, columns, cell_size, cell_size, self)

    def start_maze_solve(self):
        self.maze.solve()


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

    def draw_line_solve(self, line, fill_color = "blue"):
        cell_size = int(self.cell_size_entry.get())
        line.draw_solve(self.__canvas, fill_color, cell_size//2)



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color, size = 2):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill = fill_color, width = size)
    
    def draw_solve(self, canvas, fill_color, size):
        
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill = fill_color, width = size)

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
        self.dead_end = False
        self.num_walls = 4

    
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
        global color_selector
        color = "grey"
        if undo == True:     
            if color_selector == 0:
                color = "red"

            elif color_selector == 1:   
                color = "pink"

            elif color_selector == 2:  
                color = "orange"

            elif color_selector == 3:  
                color = "yellow"

            elif color_selector == 4:  
                color = "green"

            elif color_selector == 5:  
                color = "purple"

            elif color_selector == 6:  
                color = "indigo"

            elif color_selector == 7:  
                color = "violet"
            

        self._win.draw_line(line, color )
    
    def draw_move_solve(self, to_cell):
        color = "blue"
        p1 = Point((self._x1+self._x2)/2, (self._y1+self._y2)/2)
        p2 = Point((to_cell._x1 + to_cell._x2)/2, (to_cell._y1 + to_cell._y2)/2)
        line = Line(p1, p2)
        self._win.draw_line_solve(line, color)

class Maze:
    def __init__(self, border, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self._x1 = border
        self._y1 = border
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
        #self._break_walls_r(num_cols//2,num_rows//2)
        self._break_walls_r(num_cols-1,num_rows-1)
        self._reset_cells_visited()
        self.length = 0
        
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
                self._draw_cell_mc(i , j)
        self._win.redraw()
                
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = i*  self._cell_size_x + self._x1
        y1 = j * self._cell_size_y + self._y1
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _draw_cell_mc(self, i, j):
        if self._win is None:
            return
        x1 = i*  self._cell_size_x + self._x1
        y1 = j * self._cell_size_y + self._y1
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        #time.sleep(.05)

    def _animate_solve(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(1/(self.length+20))
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[0][0].num_walls -= 1
        self._draw_cell(0,0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._cells[self._num_cols-1][self._num_rows-1].num_walls -= 1
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
                if self._win.animation_var.get() and current != self._cells[0][0]:
                    self._draw_cell(i,j)
                else:
                    self._draw_cell_mc(i,j)
                return
            
            destination = to_visit[random.randint(0,len(to_visit)-1)]
            
            if destination == left:
                current.has_left_wall = False
                current.num_walls -= 1
                #left.num_walls -= 1
                left.has_right_wall = False
                self._break_walls_r(i-1, j )
            if destination == right:
                current.has_right_wall = False
                current.num_walls -= 1
                #right.num_walls -= 1
                right.has_left_wall = False
                self._break_walls_r( i+1, j)
            if destination == up:
                current.has_top_wall = False
                current.num_walls -= 1
                #up.num_walls -= 1
                up.has_bottom_wall = False
                self._break_walls_r( i, j-1)
            if destination == down:
                current.has_bottom_wall = False
                current.num_walls -= 1
                #down.num_walls -= 1
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
        global color_selector
        if current == self._cells[self._num_cols-1][self._num_rows-1]:
            
            return self.show_solve()
        
        if i < self._num_cols - 1:
            right = self._cells[i+1][j]
            if right.visited == False and current.has_right_wall == False:
                current.draw_move(right)
                if self._solve_r(i+1, j) == True:
                    return True
                if current.num_walls == 3:
                    color_selector += 1 % 8
                right.dead_end = True
                #print(current.num_walls)
                
                current.draw_move(right, True)
                
        if j < self._num_rows - 1:
            down = self._cells[i][j+1]
            if down.visited == False and current.has_bottom_wall == False:
                current.draw_move(down)
                if self._solve_r(i, j+1) == True:
                    return True
                if current.num_walls == 3:
                    color_selector += 1 % 8
                down.dead_end = True
                current.draw_move(down, True)
        if i > 0 :
            left = self._cells[i-1][j]
            if left.visited == False and current.has_left_wall == False:
                current.draw_move(left)
                if self._solve_r(i-1, j) == True:
                    return True
                if current.num_walls == 3:
                    color_selector += 1 % 8
                left.dead_end = True
                current.draw_move(left, True)

        if j > 0:
            up = self._cells[i][j-1]
            if up.visited == False and current.has_top_wall == False:
                current.draw_move(up)
                if self._solve_r(i, j-1) == True:
                    return True
                if current.num_walls == 3:
                    color_selector += 1 % 8
                up.dead_end = True
                current.draw_move(up, True)
        return False
    
    def show_solve(self):
        current = self._cells[0][0]
        i = 0
        j = 0
        self.length = 0 
        while current != self._cells[-1][-1]:
            self._animate_solve()
            if i < self._num_cols - 1:
                right = self._cells[i + 1][j]
                if right.visited == True and right.dead_end == False and current.has_right_wall == False:
                    current.dead_end = True
                    current.draw_move_solve(right)
                    current = right
                    i+=1
                    self.length += 1
            if j < self._num_rows - 1:
                down = self._cells[i][j+1]
                if down.visited == True and down.dead_end == False and current.has_bottom_wall == False:
                    current.dead_end = True
                    current.draw_move_solve(down)
                    current = down
                    j+=1
                    self.length += 1
            if i > 0 :
                left = self._cells[i-1][j]
                if left.visited == True and left.dead_end == False and current.has_left_wall == False:
                    current.dead_end = True
                    current.draw_move_solve(left)
                    current = left
                    i-=1
                    self.length += 1
            if j > 0:
                up = self._cells[i][j-1]
                if up.visited == True and up.dead_end == False and current.has_top_wall == False:
                    current.dead_end = True
                    current.draw_move_solve(up)
                    current = up
                    j-=1
                    self.length += 1


        return True
