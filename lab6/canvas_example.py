from tkinter import *
root = Tk()

c = Canvas(root, width=1000, height=1000, bg='white')
c.pack()

c.create_line(10, 10, 190, 50)

c.create_line(100, 180, 100, 60, fill='green',
                width=5, arrow=BOTH, dash=(10,2),
                activefill='lightgreen',
                arrowshape="10 20 10")
c.create_rectangle(10, 10, 190, 60)

c.create_rectangle(60, 80, 140, 190, fill='yellow', outline='green',
                    width=3, activedash=(5, 4))

root.mainloop()