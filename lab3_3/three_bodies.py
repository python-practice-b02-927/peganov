import graphics as gr


init = [
    {
        "m": 90000,
        "x": 300,
        "y": 300,
        "vx": 0,
        "vy": 0
    },
    {
        "m": 100,
        "x": 300,
        "y": 100,
        "vx": 20,
        "vy": 0
    },
    {
        "m": 1,
        "x": 300,
        "y": 80,
        "vx": 22.5,
        "vy": 0
    }
]


def init_1_body(config, color):
    """Creates and draws one body and initializes its velocity"""
    body_state = {}
    obj = gr.Circle(gr.Point(config['x'], config['y']), 5)
    obj.draw(window)
    obj.setFill(color)
    body_state['obj'] = obj
    body_state['vx'] = config['vx']
    body_state['vy'] = config['vy']
    body_state['color'] = color
    return body_state


def create_state(init):
    """Creates and draws bodies, initializes velocities."""
    colors = ['red', 'green', 'blue']
    bodies = []
    for config, color in zip(init, colors):
        bodies.append(
            init_1_body(config, color)
        )


def calculate_increments(state, dt):
    """Calculates dr and dv"""
    pass


def apply_increments(state, increments, dt):
    """Updates velocities and moves bodies to new positions"""
    pass


def main(init):
    dt = 0.001
    state = create_state(init)
    for i in range(10**5):
        increments = calculate_increments(state, dt)
        apply_increments(state, increments, dt)
        gr.time.sleep(dt)


window = gr.GraphWin("three bodies", 600, 600)

main(init)

window.getMouse()
window.close()
