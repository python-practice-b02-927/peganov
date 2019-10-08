import time
from random import randrange as rnd, choice
from tkinter import *


BALL_SCORE = 10
score = 0
balls = {}
remove_balls = False


def new_ball():
    x = rnd(100, 700)
    y = rnd(100, 500)
    r = rnd(30, 50)
    id_ = canv.create_oval(x-r, y-r, x+r, y+r, fill=choice(colors), width=0)
    balls[id_] = {
        "x": x,
        "y": y,
        "r": r
    }
    root.after(rnd(1000, 5000), new_ball)


def remove_random_ball():
    global remove_balls
    if remove_balls:
        if len(balls):
            id_ = choice(balls.keys())
            del balls[id_]
            canv.delete(id_)
    remove_balls = True
    root.after(rnd(1000, 10000), remove_random_ball)


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
root.geometry('800x600')

score_field = Label(root, bg='black', fg='white', text="Score: " + str(score), font=("Courier", 44))
score_field.pack()

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']

new_ball()
canv.bind('<Button-1>', click)
mainloop()
