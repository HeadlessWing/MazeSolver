from  Classes import  *

def main():
    win = Window(800,600)
    
    point_1 = Point(50, 50)
    point_2 = Point(25, 25)
    line_1 = Line(point_1, point_2)
    win.draw_line(line_1, "black")
    point_3 = Point(75, 10)
    point_4 = Point(10, 75)
    line_2 = Line(point_3, point_4)
    win.draw_line(line_2, "black")

    cell1 = Cell(win)
    cell2 = Cell(win)
    cell3 = Cell(win)

    cell1.draw(50, 50, 100, 100)
    cell2.draw(100, 100, 150, 150)
    cell3.draw(0, 50, 50, 100 )
    cell1.draw_move(cell2, True)

    maze = Maze(100, 100, 10, 10, 50, 50, win)

    win.wait_for_close()

    
if __name__ == "__main__":
    main()
    