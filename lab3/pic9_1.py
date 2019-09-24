import graphics as gr


def draw_snowman(win):
    pass


def draw_ice_hole(win):
    pass


def draw_fishing_rod(win):
    pass


def draw_background(win):
    """Draws sky and snow"""
    sky = gr.Rectangle(gr.Point(-10, -10), gr.Point(610, 500))
    sky.setFill('blue')
    snow = gr.Rectangle(gr.Point(-10, 500), gr.Point(610, 1000))
    snow.setFill('white')
    sky.draw(win)
    snow.draw(win)


def draw_fish(win):
    pass


def draw_star(win):
    pass


def main(win):
    """Draws picture"""
    draw_background(win)
    draw_snowman(win)
    draw_ice_hole(win)
    draw_fishing_rod(win)
    draw_fish(win)
    draw_star(win)


w = gr.GraphWin('pic9_1', 600, 1000)

main(w)
w.getMouse()
w.close()

