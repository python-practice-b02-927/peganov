import time
from random import randrange as rnd, choice
from tkinter import *


BALL_SCORE = 10
score = 0


def new_ball():
    global x, y, r, score
    canv.delete(ALL)
    x = rnd(100, 700)
    y = rnd(100, 500)
    r = rnd(30, 50)
    canv.create_oval(x-r, y-r, x+r, y+r, fill=choice(colors), width=0)
    root.after(1000, new_ball)


def distance(a, b):
    return ((a[0]-b[0])**2 + (a[1] - b[1])**2)**0.5


def click(event):
    global score
    if distance([event.x, event.y], [x, y]) <= r:
        score += BALL_SCORE
        score_field['text'] = "Score: " + str(score)


root = Tk()
root.geometry('800x600')

score_field = Label(root, bg='black', fg='white', text="Score: " + str(score))
score_field.pack()

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']

new_ball()
canv.bind('<Button-1>', click)
mainloop()
