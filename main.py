from  Classes import  *
import sys

def main():
    sys.setrecursionlimit(10000)
    win = Window(800,600)
    maze = Maze(100, 100, 50, 100, 25, 25, win)

    maze._break_entrance_and_exit()
    maze._break_walls_r(0,0)

    win.wait_for_close()

    
if __name__ == "__main__":
    main()
    