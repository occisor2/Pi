import curses
import time
import tracemalloc

def gospers_pi():
    q,r,t,n,i = 1,0,1,8,1
    while True:
        if n == (q*(675*i-216)+125*r)//(125*t):
            yield n
            q,r = 10*q,10*r-10*n*t
        else:
            q,r,t,i = i*(2*i-1)*q,3*(3*i+1)*(3*i+2)*((5*i-2)*q+r),3*(3*i+1)*(3*i+2)*t,i+1
            n = (q*(27*i-12)+5*r) // (5*t)

if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(True)

    tracemalloc.start(10)
    stats: list[tracemalloc.Statistic] = []
    pi = gospers_pi()

    ymax, xmax = stdscr.getmaxyx()
    y, x = 2, 0
    index = 0
    digits = 0
    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break

        t1 = time.perf_counter_ns()
        digit = next(pi)
        t2 = time.perf_counter_ns()
        execTime = (t2 - t1) / 1000000
        # Only take a snapshot at set intervals to prevent slowdown
        if (index == 0):
            snap = tracemalloc.take_snapshot()
            stats = snap.statistics('traceback')
            index = 500
        digits += 1

        if (x >= xmax - 1):
            x = 0
            y += 1
        if (y >= ymax - 1):
            stdscr.clear()
            y = 2

        stdscr.addch(y, x, str(digit))
        x += 1

        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, f'digits: {digits}, time:{execTime: 010} ms,\
 memory:{stats[0].size / (1024 * 1024): 015} MiB')
        stdscr.refresh()

        index -= 1
        #time.sleep(0.001)

    tracemalloc.stop()
    curses.endwin()
