from pyray import *
import serial
from time import time
import os


absolute_path=file_path = os.path.abspath(__file__).replace("main.py","float.png")
relative_path = os.path.relpath(absolute_path) 
print(relative_path) 
init_window(400, 800, "FLOAT SIM")
set_target_fps(60)
image = load_image(relative_path)
texture = load_texture_from_image(image)    
doserial = True
if doserial:    
    ser = serial.Serial('COM10', 9600, timeout=10)

def getScreenY(y):
    return ((y * 170) + L)

L = 100  
G = 9.8  
S = 9.8+3.7765 
M = 6.8
Y = 0
V = 0 
sub = 0

set_trace_log_level(TraceLogLevel.LOG_ERROR) 

while not window_should_close():
    if doserial:
        ser.write((str(Y) + "\n").encode())
        if ser.in_waiting > 0:
            LINE = ser.readline().decode(encoding="utf-8")
        
            M = 6.8 + ((float(LINE) / 180) * 8) 

    dt = get_frame_time()
    total_force = M * G

    if is_mouse_button_pressed(0):
        M += 1
    if is_mouse_button_pressed(1):
        M -= 1
    screen_y = getScreenY(Y)
    if screen_y + 20 > L:
        
        sub = max(0, min(1.0, (screen_y + 20 - L) / 40.0))
        
        
        total_force -= ((S) * sub * 10) 
        
        
        V *= 1 - (sub * 0.05)

    
    A = total_force / M
    
    
    V += A * dt
    Y += V * dt

    
    if Y > 4:
        Y = 4
        V *= -0.1

    begin_drawing()
    clear_background(RAYWHITE)
    
    
    draw_rectangle(0, int(L), 400, 800 - int(L), BLUE)
    #draw_line(200 - 20, int(getScreenY(Y))-20,200 - 20, int(getScreenY(Y))-20+int(G*M),GREEN)
    draw_line(0, 525, 400, 525, BLACK)
    #draw_rectangle(200 - 20, int(getScreenY(Y)) - 20, 40, 40, RED)
    draw_texture(texture,200 - 20, int(getScreenY(Y))-20,WHITE)
    draw_text(str(round(Y, 2)), 10, 10, 20, BLACK)
    draw_text(str(round(M, 2)), 10, 35, 20, BLACK)
    
    end_drawing()

close_window()