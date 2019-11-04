import time
from random import randrange as rnd, choice
from tkinter import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BALL_SCORE = 10
# time increment in milliseconds
DT = 10
score = 0
balls = {}
remove_balls = False


def create_random_ball():
    x = rnd(100, 700)
    y = rnd(100, 500)
    r = rnd(30, 50)
    # ball velocity in points per second
    vx = rnd(-100, 100)
    vy = rnd(-100, 100)
    id_ = canv.create_oval(x - r, y - r, x + r, y + r, fill=choice(colors), width=0)
    return id_, {"x": x, "y": y, "r": r, "vx": vx, "vy": vy}


def launch_random_balls_creation():
    id_, ball_spec = create_random_ball()
    balls[id_] = ball_spec
    root.after(rnd(1000, 5000), launch_random_balls_creation)


def create_ball(x, y, vx, vy, r, color):
    id_ = canv.create_oval(x - r, y - r, x + r, y + r, fill=color, width=0)
    return 


def remove_random_ball():
    global remove_balls
    if remove_balls:
        if len(balls):
            id_ = choice(balls.keys())
            del balls[id_]
            canv.delete(id_)
    remove_balls = True
    root.after(rnd(1000, 10000), remove_random_ball)


def bounce_1_direction(x, vx, dx, r, width):
    if vx > 0:
        if x + r + dx > width:
            vx = -vx
            x = 2 * width - 2 * r - (x + dx)
        else:
            x += dx
    else:
        if x - r + dx < 0:
            vx = -vx
            x = 2 * r - x - dx
        else:
            x = x + dx
    return x, vx


def move_balls():
    ids = list(balls.keys())
    canv.delete(ALL)
    for id_ in ids:
        b = balls[id_]
        dx = b['vx'] * DT / 1000
        dy = b['vy'] * DT / 1000
        x, vx = bounce_1_direction(b['x'], b['vx'], dx, b['r'], WINDOW_WIDTH)
        y, vy = bounce_1_direction(b['y'], b['vy'], dy, b['r'], WINDOW_HEIGHT)
        del balls[id_]


def distance(a, b):
    return ((a[0]-b[0])**2 + (a[1] - b[1])**2)**0.5


def click(event):
    global score
    ids = list(balls.keys())
    for id_ in ids:
        if distance([event.x, event.y], [balls[id_]['x'], balls[id_]['y']]) <= balls[id_]['r']:
            score += BALL_SCORE
            score_field['text'] = "Score: " + str(score)
            del balls[id_]
            canv.delete(id_)


root = Tk()
root.geometry(str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT))

score_field = Label(root, bg='black', fg='white', text="Score: " + str(score), font=("Courier", 44))
score_field.pack()

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']

launch_random_balls_creation()
canv.bind('<Button-1>', click)
mainloop()
