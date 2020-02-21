import math

import graphics as gr


def draw_planet(window, x, y, r):
    center = gr.Point(x, y)
    planet = gr.Circle(center, r)
    planet.setOutline('SkyBlue1')
    planet.setFill('blue')
    planet.draw(window)


def get_vector_endpoint(x0, y0, length, alpha):
    delta_x = length * math.cos(alpha)
    delta_y = length * math.sin(alpha)
    return x0 + delta_x, y0 + delta_y


def draw_triangle(window, x, y, a, b, alpha, beta, color):
    x1, y1 = get_vector_endpoint(x, y, a, alpha)
    x2, y2 = get_vector_endpoint(x, y, b, beta)
    print(x, y, x1, y1, x2, y2)
    triangle = gr.Polygon(gr.Point(x, y), gr.Point(x1, y1), gr.Point(x2, y2))
    triangle.setFill(color)
    triangle.setOutline(color)
    triangle.draw(window)


def draw_destroyer(window, x, y, length):
    spine_angle = math.pi / 12
    right_base_edge_angle = math.pi/12 + math.pi/2
    left_base_edge_angle = -math.pi / 6
    spine_length = length
    left_base_edge_length = length / 6
    right_base_edge_length = length / 3

    draw_triangle(window, x, y, spine_length, right_base_edge_length, spine_angle, right_base_edge_angle, 'dim gray')
    draw_triangle(window, x, y, spine_length, left_base_edge_length, spine_angle, left_base_edge_angle, 'gray')


def draw_sun(window, x, y, r):
    center = gr.Point(x, y)
    sun = gr.Circle(center, r)

    sun.setFill('white')
    sun.setOutline('yellow')
    sun.draw(window)


def draw_all(window):
    window.setBackground('black')
    draw_planet(window, 1200, -1000, 1400)
    draw_destroyer(window, 200, 300, 600)
    draw_sun(window, 100, 100, 50)


window = gr.GraphWin("Star destroyer", 800, 600)

draw_all(window)

window.getMouse()
window.close()

