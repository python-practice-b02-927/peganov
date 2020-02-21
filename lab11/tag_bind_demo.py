import tkinter as tk


def callback1(event):
    print(1, event.x, event.y)


def callback2(event):
    print(2, event.x, event.y)


root = tk.Tk()
frame = tk.Frame()
frame.pack(fill=tk.BOTH, expand=1)
canvas = tk.Canvas()
canvas.pack(fill=tk.BOTH, expand=1)

rect1 = canvas.create_rectangle(10, 10, 110, 110, fill='red')
rect2 = canvas.create_rectangle(60, 60, 160, 160, fill='blue')

canvas.tag_bind(rect1, '<Button-1>', callback1)
canvas.tag_bind(rect2, '<Button-1>', callback2)

root.mainloop()
