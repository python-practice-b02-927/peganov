from tkinter import *

class BattleField(Canvas):
    def __init__(self, master):
        super().__init__(master)
        self.gun = 'foo'

class Application(Tk):
    def __init__(self, my_data):
        # С помощью `super()` вызывают методы родительских классов
        # Вызов `__init__()` родителя важен, так как соединяет объект
        # с родительским виджетом.
        super().__init__()
        self.my_data = my_data
        self.battlefield = BattleField(self)
        self.battlefield.pack()

app = Application('bar')
app.mainloop()