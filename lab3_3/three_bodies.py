import graphics as gr


init_classic_orbits = [
    {
        "m": 360000,
        "x": 300,
        "y": 300,
        "vx": 0,
        "vy": 0
    },
    {
        "m": 400,
        "x": 300,
        "y": 100,
        "vx": 30,
        "vy": 0
    },
    {
        "m": 1,
        "x": 300,
        "y": 200,
        "vx": 30,
        "vy": 0
    }
]


init_2_bodies = [
    {
        "m": 10**6,
        "x": 300,
        "y": 150,
        "vx": 25,
        "vy": 0
    },
    {
        "m": 10**6,
        "x": 300,
        "y": 450,
        "vx": -25,
        "vy": 0
    }
]


init_double_planet = [
    {
        "m": 10**7,
        "x": 300,
        "y": 300,
        "vx": -46,
        "vy": 0
    },
    {
        "m": 10**6,
        "x": 300,
        "y": 100,
        "vx": 103,
        "vy": 0
    },
    {
        "m": 10**6,
        "x": 300,
        "y": 70,
        "vx": 263,
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
    body_state['m'] = config['m']
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
    return bodies


def calculate_one_body_increments(target, other, dt):
    """Calculates increments in position and velocity for 1 body"""
    increments = {
        "x": 0,
        "y": 0,
        "vx": 0,
        "vy": 0
    }
    for b in other:
        t_center = target['obj'].getCenter()
        b_center = b['obj'].getCenter()
        d = (
            (t_center.x - b_center.x)**2 +
            (t_center.y - b_center.y)**2
        )**0.5
        abs_force = target['m'] * b['m'] / d**2
        force_direction = [
            (b_center.x - t_center.x) / d,
            (b_center.y - t_center.y) / d
        ]
        force = [
            force_direction[0] * abs_force,
            force_direction[1] * abs_force
        ]
        accelaration = [
            force[0] / target['m'],
            force[1] / target['m']
        ]
        increments['vx'] += accelaration[0] * dt
        increments['vy'] += accelaration[1] * dt
    increments['x'] += target['vx'] * dt
    increments['y'] += target['vy'] * dt
    return increments


def calculate_increments(state, dt):
    """Calculates dr and dv"""
    increments = []
    num_bodies = len(state)
    for i in range(num_bodies):
        increments.append(
            calculate_one_body_increments(state[i], state[:i]+state[i+1:], dt)
        )
    return increments


def add_trajectory_point(body_state):
    center = body_state['obj'].getCenter()
    p = gr.Point(center.x, center.y)
    p.setOutline(body_state['color'])
    p.setFill(body_state['color'])
    p.draw(window)


def add_trajectory_points(state):
    for b_state in state:
        add_trajectory_point(b_state)


def apply_increments(state, increments):
    """Updates velocities and moves bodies to new positions"""
    for i, (b_state, b_inc) in enumerate(zip(state, increments)):
        b_state['vx'] += b_inc['vx']
        b_state['vy'] += b_inc['vy']
        b_state['obj'].change_movement_direction(b_inc['x'], b_inc['y'])


def main(init):
    dt = 0.0001
    state = create_state(init)
    for i in range(int(1 / dt)*100):
        increments = calculate_increments(state, dt)
        apply_increments(state, increments)
        if i % (0.025 / dt) == 0:
            add_trajectory_points(state)
        gr.time.sleep(dt)


window = gr.GraphWin("three bodies", 600, 600)

main(init_double_planet)
# main(init_classic_orbits)
# main(init_2_bodies)

window.getMouse()
window.close()
