import asyncio
from pyray import *
import os
from math import dist
import colorutils
import matplotlib.pyplot as plt

# run command before main.py: export DISPLAY=:0
def processColor(c, o):
    color = colorutils.hex_to_rgb("#" + c)
    return Color(color[0], color[1], color[2], o)

X, Y = 0, 1

def scale(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def scaleInt(value, istart, istop, ostart, ostop):
    return int(ostart + (ostop - ostart) * ((value - istart) / (istop - istart)))

R_GREEN = processColor("3FCC2C", 255)
W_PURPLE = processColor("4E008E", 255)
W_PURPLE2 = processColor("7F2C92", 255)

width, height = 1366, 768 - 45 - 30

profiles = [[(0, 0), (5, 1), (10, 2), (15, 3)], [(0, 3), (5, 2), (10, 1), (15, 0)]]

def circleButton(x, y, radius, image, color):
    draw_circle(x, y, radius, color)
    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
        if dist((get_mouse_x(), get_mouse_y()), (x, y)) <= radius:
            return True
    return False
    
mainfont = "mononoki-Regular.ttf"

# --- Initialization Phase ---
init_window(width, height, "soup")
font = load_font_ex(("float_graphing_UI/" + mainfont).encode(), 30, None, 0)
current_profile = 0

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)

    if circleButton(789, 135, 25, NotImplemented, R_GREEN):
        # Your previous logic for generating the graph
        x_values = []
        y_values = []
        for p in profiles[current_profile]:
            x_values.append(p[X])
            y_values.append(p[Y])
        
        # Save the plot to a file instead of displaying it.
        plt.plot(x_values, y_values)
        plt.xlabel("X-axis Label")
        plt.ylabel("Y-axis Label")
        plt.title("Simple Line Plot")
        plt.savefig("profile_graph.png")
        plt.close() # Close the plot to free memory

    draw_line(0, 36, width, 36, WHITE)
    draw_line(36, 36, 36, height, WHITE)
    draw_line(660, 36, 660, height, WHITE)

    for i in range(len(profiles)):
        draw_rectangle(0, 37 + (36 * i), 35, 36, (W_PURPLE, W_PURPLE2)[i % 2])
        draw_text_ex(font, str(i + 1), Vector2(10, 42 + (36 * i)), 25, 2, WHITE)

    if get_mouse_x() <= 36:
        for i in range(len(profiles)):
            if get_mouse_y() > 37 + (36 * i) and get_mouse_y() < 36 + 37 + (36 * i):
                draw_rectangle_lines(0, 37 + (36 * i), 35, 36, WHITE)
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    draw_rectangle(0, 37 + (36 * i), 35, 36, WHITE)
                    current_profile = i
    
    draw_line(36, 72, 658, 72, WHITE)
    draw_line(348, 72, 348, height, WHITE)

    for point in profiles[current_profile]:
        I = profiles[current_profile].index(point)
        draw_text_ex(font, str(point[Y]) + "(s)", Vector2(350, I * 30 + 72), 20, 2, WHITE)
        draw_text_ex(font, str(point[X]) + "(m)", Vector2(40, I * 30 + 72), 20, 2, WHITE)
        draw_line(36, I * 30 + 94, 658, I * 30 + 94, WHITE)
    
    draw_fps(300, 0)
    end_drawing()

close_window()