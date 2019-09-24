import graphics as gr


def draw_snowman(win):
    pass


def draw_ice_hole(win):
    pass


def draw_fishing_rod(win):
    pass


def draw_background(win):
    pass


def draw_fish(win):
    pass


def draw_star(win):
    pass


def main(win):
    """Draws picture"""
    draw_snowman(win)
    draw_ice_hole(win)
    draw_fishing_rod(win)
    draw_background(win)
    draw_fish(win)
    draw_star(win)


w = gr.GraphWin('pic9_1', 600, 1000)

main(w)
w.getMouse()
w.close()

