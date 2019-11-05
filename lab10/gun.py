import json
import math
import os
import tkinter as tk
from abc import ABC, abstractmethod
from random import randrange as rnd, choice
from tkinter import filedialog

import hit_check


# Time step for delayed jobs
DT = 30
VICTORY_MSG_TIME = 3000
WINDOW_SHAPE = (800, 600)


def pass_event(event):
    pass


class Agent(ABC):
    def __init__(self):
        self.job = None

    @abstractmethod
    def start(self):
        self.job = self.canvas.after(DT, self.update)

    @abstractmethod
    def play(self):
        if self.job == 'pause':
            self.job = self.canvas.after(DT, self.update)

    @abstractmethod
    def stop(self):
        if self.job is not None:
            self.canvas.after_cancel(self.job)
            self.job = None

    @abstractmethod
    def pause(self):
        if self.job is not None and self.job != 'pause':
            self.canvas.after_cancel(self.job)
            self.job = 'pause'

    @abstractmethod
    def update(self):
        pass


class Ball(Agent):
    def __init__(self, canvas, x, y, vx, vy):
        super().__init__()
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 100
        self.canvas.bullets[self.id] = self
        # Используется для определения номера выстрела, которым уничтожена
        # цель.
        self.bullet_number = self.canvas.get_bullet_number()

    def start(self):
        super().start()

    def play(self):
        super().play()

    def stop(self):
        super().stop()

    def pause(self):
        super().pause()

    def update(self):
        self.x += self.vx
        self.y -= self.vy
        self.set_coords()
        targets_hit = self.hit_targets()
        if targets_hit:
            self.destroy()
        else:
            self.live -= 1
            if self.live > 0:
                self.job = self.canvas.after(DT, self.update)
            else:
                self.destroy()

    def destroy(self):
        self.stop()
        self.canvas.delete(self.id)
        del self.canvas.bullets[self.id]

    def set_coords(self):
        self.canvas.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def hit_targets(self):
        ids_hit = []
        for t_id, t in list(self.canvas.targets.items()):
            if hit_check.is_hit(
                    (self.x, self.y),
                    self.r,
                    (-self.vx, -self.vy),
                    (t.x, t.y),
                    t.r
            ):
                self.canvas.report_hit(self, t)
                ids_hit.append(t_id)
                t.destroy()
        return ids_hit

    def get_state(self):
        state = {
            "x": self.x,
            "y": self.y,
            "vx": self.vx,
            "vy": self.vy,
            "r": self.r,
            "color": self.color,
            "live": self.live,
            "job": self.job is not None
        }
        return state


class Gun(Agent):
    def __init__(self, canvas):
        super().__init__()

        self.gun_velocity = 1
        self.gun_power_gain = 1
        self.min_gun_power = 10
        self.max_gun_power = 70
        self.zero_power_length = 20

        self.gun_coords = [20, 450]
        self.vy = 0
        self.mouse_coords = [None, None]
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1

        self.canvas = canvas
        self.id = self.canvas.create_line(
            *self.gun_coords, *self.get_gunpoint(), width=7)

        self.job = None

    def start(self):
        self.bind_all()
        super().start()

    def play(self):
        if self.job == 'pause':
            self.bind_all()
        super().play()

    def stop(self):
        super().stop()
        self.unbind_all()
        self.vy = 0
        self.f2_power = 10
        self.f2_on = 0
        self.mouse_coords = [None, None]

    def pause(self):
        super().pause()
        self.unbind_all()
        self.mouse_coords = [None, None]

    def update(self):
        self.gun_coords[1] += self.vy
        self.update_angle()
        if self.f2_on:
            self.f2_power = min(
                self.f2_power + self.gun_power_gain, self.max_gun_power)
        else:
            self.f2_power = self.min_gun_power
        self.redraw()
        self.job = self.canvas.after(DT, self.update)

    def update_angle(self):
        self.mouse_coords = self.canvas.get_mouse_coords()
        dx = self.mouse_coords[0]-self.gun_coords[0]
        dy = self.mouse_coords[1]-self.gun_coords[1]
        if dx != 0:
            self.an = math.atan(dy / dx)
        else:
            self.an = 1

    def get_gunpoint(self):
        length = self.f2_power + self.zero_power_length
        x = self.gun_coords[0] + length * math.cos(self.an)
        y = self.gun_coords[1] + length * math.sin(self.an)
        return x, y

    def redraw(self):
        self.canvas.coords(
            self.id,
            *self.gun_coords,
            *self.get_gunpoint()
        )
        if self.f2_on:
            self.canvas.itemconfig(self.id, fill='orange')
        else:
            self.canvas.itemconfig(self.id, fill='black')

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        self.update_angle()
        bullet_vx = self.f2_power * math.cos(self.an)
        bullet_vy = -self.f2_power * math.sin(self.an)
        bullet = Ball(self.canvas, *self.get_gunpoint(), bullet_vx, bullet_vy)
        bullet.start()
        self.f2_on = 0
        self.f2_power = 10

    def set_movement_direction_to_up(self, event):
        self.vy = -self.gun_velocity

    def set_movement_direction_to_down(self, event):
        self.vy = self.gun_velocity

    def stop_movement(self, event):
        self.vy = 0

    def bind_all(self):
        self.canvas.bind('<Button-1>', self.fire2_start, add='')
        self.canvas.bind('<ButtonRelease-1>', self.fire2_end, add='')

        root = self.canvas.get_root()
        root.bind('<Up>', self.set_movement_direction_to_up, add='')
        root.bind('<KeyRelease-Up>', self.stop_movement, add='')
        root.bind('<Down>', self.set_movement_direction_to_down, add='')
        root.bind('<KeyRelease-Down>', self.stop_movement, add='')

    def unbind_all(self):
        self.canvas.bind('<Button-1>', pass_event, add='')
        self.canvas.bind('<ButtonRelease-1>', pass_event, add='')
        root = self.canvas.get_root()
        root.bind('<Up>', pass_event, add='')
        root.bind('<KeyRelease-Up>', pass_event, add='')
        root.bind('<Down>', pass_event, add='')
        root.bind('<KeyRelease-Down>', pass_event, add='')

    def get_state(self):
        state = {
            "gun_coords": self.gun_coords,
            "vy": self.vy,
            "mouse_coords": self.mouse_coords,
            "f2_power": self.f2_power,
            "f2_on": self.f2_on,
            "an": self.an,
            "job": self.job is not None
        }
        return state


class Target(Agent):
    def __init__(self, canvas):
        super().__init__()

        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'

        self.canvas = canvas
        self.id = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color)

    def start(self):
        super().start()

    def play(self):
        super().play()

    def stop(self):
        super().stop()

    def pause(self):
        super().pause()

    def update(self):
        self.job = self.canvas.after(DT, self.update)

    def destroy(self):
        self.stop()
        self.canvas.delete(self.id)
        del self.canvas.targets[self.id]

    def get_state(self):
        state = {
            "x": self.x,
            "y": self.y,
            "r": self.r,
            "color": self.color,
            "job": self.job is not None
        }
        return state


class BattleField(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, background='white')

        self.num_targets = 2

        self.gun = Gun(self)
        self.targets = {}
        self.bullets = {}

        # Переменная для присвоения номеров выпущенным пулям.
        # Номера используются для определения, каким по счету выстрелом была
        # уничтожена цель. Отсчет начинается с единицы.
        self.bullet_counter = 0
        self.last_hit_bullet_number = None
        self.victory_text_id = self.create_text(
            WINDOW_SHAPE[0] // 2, WINDOW_SHAPE[1] // 2, text='', font='28')

        self.catch_victory_job = None
        self.canvas_restart_job = None

    def remove_targets(self, targets_to_remove=None):
        if targets_to_remove is None:
            ids = list(self.targets)
        else:
            ids = list(targets_to_remove)
        for id_ in ids:
            # Не нужно удалять элемент словаря `self.targets`, так как удаление
            # осуществляется в методе `Target.destroy()`.
            self.targets[id_].destroy()

    def remove_bullets(self, bullets_to_remove=None):
        if bullets_to_remove is None:
            ids = list(self.bullets)
        else:
            ids = list(bullets_to_remove)
        for id_ in ids:
            # Не нужно удалять элемент словаря `self.bullets`, так как удаление
            # осуществляется в методе `Ball.destroy()`.
            self.bullets[id_].destroy()

    def create_targets(self):
        for _ in range(self.num_targets):
            t = Target(self)
            self.targets[t.id] = t

    def start(self):
        self.catch_victory_job = self.after(DT, self.catch_victory)
        self.gun.start()
        for t in self.targets.values():
            t.start()
        for b in self.bullets.values():
            b.start()

    def play_jobs(self):
        if self.catch_victory_job == 'pause':
            self.catch_victory_job = self.after(DT, self.catch_victory)
        if self.canvas_restart_job == 'pause':
            self.canvas_restart_job = self.after(
                VICTORY_MSG_TIME, self.restart)

    def play(self):
        self.play_jobs()
        self.gun.play()
        for t in self.targets.values():
            t.play()
        for b in self.bullets.values():
            b.play()

    def stop(self):
        self.gun.stop()
        for t in self.targets.values():
            t.stop()
        for b in self.bullets.values():
            b.stop()
        if self.catch_victory_job is not None:
            self.after_cancel(self.catch_victory_job)
            self.catch_victory_job = None
        if self.canvas_restart_job is not None:
            self.after_cancel(self.canvas_restart_job)
            self.canvas_restart_job = None

    def pause_jobs(self):
        if self.catch_victory_job is not None:
            self.after_cancel(self.catch_victory_job)
            self.catch_victory_job = 'pause'
        if self.canvas_restart_job is not None:
            self.after_cancel(self.canvas_restart_job)
            self.canvas_restart_job = 'pause'

    def pause(self):
        self.gun.pause()
        for t in self.targets.values():
            t.pause()
        for b in self.bullets.values():
            b.pause()
        self.pause_jobs()

    def restart(self):
        self.stop()
        self.itemconfig(self.victory_text_id, text='')
        self.remove_targets()
        self.remove_bullets()
        self.create_targets()
        self.bullet_counter = 0
        self.start()

    def get_root(self):
        root = self.master
        while root.master is not None:
            root = root.master
        return root

    def get_mouse_coords(self):
        abs_x = self.winfo_pointerx()
        abs_y = self.winfo_pointery()
        canvas_x = self.winfo_rootx()
        canvas_y = self.winfo_rooty()
        return [abs_x - canvas_x, abs_y - canvas_y]

    def show_victory_text(self):
        self.itemconfig(
            self.victory_text_id,
            text='Вы уничтожили цели {}-м выстрелом'.format(
                self.last_hit_bullet_number))
        self.canvas_restart_job = self.after(VICTORY_MSG_TIME, self.restart)

    def catch_victory(self):
        """Завершает раунда и показывает сколько выстрелов потребовалось,
        чтобы сбить цели.
        """
        if not self.targets:
            self.catch_victory_job = None
            self.stop()
            self.show_victory_text()
        else:
            self.catch_victory_job = self.after(DT, self.catch_victory)

    def get_bullet_number(self):
        self.bullet_counter += 1
        return self.bullet_counter

    def report_hit(self, bullet, target):
        self.last_hit_bullet_number = bullet.bullet_number
        self.master.report_hit(bullet, target)

    def get_state(self):
        state = {
            "gun": self.gun.get_state(),
            "targets": [t.get_state() for t in self.targets.values()],
            "bullets": [b.get_state() for b in self.bullets.values()],
            "bullet_counter": self.bullet_counter,
            "last_hit_bullet_number": self.last_hit_bullet_number,
            "victory_text": self.itemcget(self.victory_text_id, 'text'),
            "catch_victory_job": self.catch_victory_job is not None,
            "canvas_restart_job": self.canvas_restart_job is not None
        }
        return state


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.score = 0
        self.score_tmpl = 'Score: {}'
        self.score_label = tk.Label(
            self,
            text=self.score_tmpl.format(self.score),
            font=("Times New Roman", 36)
        )
        self.score_label.pack()

        self.battlefield = BattleField(self)
        self.battlefield.pack(fill=tk.BOTH, expand=1)

    def new_game(self):
        self.score = 0
        self.score_label['text'] = self.score_tmpl.format(self.score)
        self.battlefield.restart()

    def report_hit(self, bullet, target):
        self.score += 1
        self.score_label['text'] = self.score_tmpl.format(self.score)

    def pause(self):
        self.battlefield.pause()

    def play(self):
        self.battlefield.play()

    def get_state(self):
        state = {
            'score': self.score,
            'battlefield': self.battlefield.get_state()
        }
        return state


class Menu(tk.Menu):
    def __init__(self, master, game):
        super().__init__(master)

        self.game = game

        self.file_menu = tk.Menu(self)
        self.file_menu.add_command(label="save", command=self.master.save)
        self.file_menu.add_command(label="load", command=self.master.load)
        self.add_cascade(label="file", menu=self.file_menu)

        self.game_menu = tk.Menu(self)
        self.game_menu.add_command(label="new", command=self.master.new_game)
        self.add_cascade(label="game", menu=self.game_menu)


class GunGameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('{}x{}'.format(*WINDOW_SHAPE))

        # Переменная `__file__` содержит путь к файлу, в котором используется.
        #
        # Функция `os.path.split()` разделяет путь к файлу на имя директории
        # и имя файла.
        #
        # Функция `os.path.join()` объединяет несколько путей в один. Она
        # самостоятельно подбирает разделитель в соответствии с операционной
        # системой: '/' для UNIX и '\' для Windows.
        self.save_dir = os.path.join(os.path.split(__file__)[0], 'save')

        self.main_frame = MainFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.menu = Menu(self.master, self)
        self.config(menu=self.menu)

        self.bind("<Control-s>", self.save)

    def get_state(self):
        return {'main_frame': self.main_frame.get_state()}

    def get_save_file_name(self):
        os.makedirs(self.save_dir, exist_ok=True)
        file_name = filedialog.asksaveasfilename(
            initialdir=self.save_dir,
            title='Save game',
            filetypes=(("json files", "*.json"), ("all files", "*.*"))
        )
        if file_name in [(), '']:
            return None
        return file_name

    def save(self, event=None):
        self.pause()
        game_state = self.get_state()
        file_name = self.get_save_file_name()
        if file_name is not None:
            with open(file_name, 'w') as f:
                # Аргумент `indent` обеспечивает за красивое
                # оформление JSON файла.
                json.dump(game_state, f, indent=2)
        self.play()

    def load(self):
        pass  # TODO

    def new_game(self):
        self.main_frame.new_game()

    def pause(self):
        self.main_frame.pause()

    def play(self):
        self.main_frame.play()


app = GunGameApp()
app.new_game()
app.mainloop()
