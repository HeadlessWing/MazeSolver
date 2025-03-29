from  Classes import  *
import sys

def main():
    sys.setrecursionlimit(10000)
    win = Window(1920,1200)
    maze = Maze(10, 10, 50, 50, 10, 10, win)

    win.wait_for_close()

    
if __name__ == "__main__":
    main()
    