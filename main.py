from  Classes import  *
import sys

def main():
    sys.setrecursionlimit(10000)
    win = Window(1920,1200)
    maze = Maze(10, 10, 10, 15, 100, 100, win)

    win.wait_for_close()

    
if __name__ == "__main__":
    main()
    