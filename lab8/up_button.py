import tkinter as tk


def up_button(event):
  lbl['text'] = 'up'


def up_button_release(event):
  lbl['text'] = 'None'


root = tk.Tk()
lbl = tk.Label(root, text='None')
lbl.pack()

root.bind('<Up>', up_button)
root.bind('<KeyRelease-Up>', up_button_release)

root.mainloop()

