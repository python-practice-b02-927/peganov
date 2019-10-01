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


def init_1_body(config):
    """Creates and draws one body and initializes its velocity"""
    pass


def create_state(init):
    """Creates and draws bodies, initializes velocities."""
    bodies = []
    for config in init:
        bodies.append(init_1_body(config))


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


window = gr.GraphWin("three bodies", 600, 600)

main(init)

window.getMouse()
window.close()
