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


def main(init):
    pass


window = gr.GraphWin("three bodies", 600, 600)

main(init)

window.getMouse()
window.close()
