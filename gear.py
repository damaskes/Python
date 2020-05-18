import tkinter as tk
import math

WIDTH = 400
HEIGHT = 400
CANVAS_MID_X = WIDTH / 2
CANVAS_MID_Y = HEIGHT / 2
SIDE = WIDTH / 4
CENTER = (CANVAS_MID_X, CANVAS_MID_Y)
OVAL_CORDS = [CANVAS_MID_X - 40, CANVAS_MID_Y - 40, CANVAS_MID_X + 40, CANVAS_MID_Y + 40]

vertices = [
    [CANVAS_MID_X - SIDE / 2, CANVAS_MID_Y - SIDE / 2],
    [CANVAS_MID_X + SIDE / 2, CANVAS_MID_Y - SIDE / 2],
    [CANVAS_MID_X + SIDE / 2, CANVAS_MID_Y + SIDE / 2],
    [CANVAS_MID_X - SIDE / 2, CANVAS_MID_Y + SIDE / 2],
]


def rotate(points, angle, center_):
    angle = math.radians(angle)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    cx, cy = center_
    new_points = []
    for x_old, y_old in points:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        new_points.append([x_new + cx, y_new + cy])
    return new_points


root = tk.Tk()
canvas = tk.Canvas(root, bg="black", height=HEIGHT, width=WIDTH)
canvas.pack()
for e in range(0, 90, 30):
    canvas.create_polygon(rotate(vertices, e, CENTER), fill='#3C3F41')
canvas.create_oval(OVAL_CORDS[0], OVAL_CORDS[1], OVAL_CORDS[2], OVAL_CORDS[3], fill='black')

root.mainloop()
