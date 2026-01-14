from pyray import *
import serial
from time import time

init_window(400, 800, "goob")
set_target_fps(60)

doserial = False
if doserial:    
    ser = serial.Serial('COM5', 9600, timeout=10)

def getScreenY(y):
    return ((y * 170) + L)

L = 100  
G = 9.8  
S = 3.7765 
M = 6.8
Y = -1.0 
V = 0.0  
sub = 0

set_trace_log_level(TraceLogLevel.LOG_ERROR) 

while not window_should_close():
    if doserial:
        ser.write((str(int(Y * 100) / 100) + "\n").encode())
        if ser.in_waiting > 0:
            LINE = ser.readline().decode(encoding="utf-8")
            
            M = max(0.1, ((float(LINE) / 180) * 300)) 

    dt = get_frame_time()
    total_force = M * G

    
    screen_y = getScreenY(Y)
    if screen_y + 20 > L:
        
        sub = max(0, min(1.0, (screen_y + 20 - L) / 40.0))
        
        
        total_force -= ((M+S) * sub * 10) 
        
        
        V *= 1 - (sub * 0.05)

    
    A = total_force / M
    
    
    V += A * dt
    Y += V * dt

    
    if Y > 4:
        Y = 4
        V *= -0.5

    begin_drawing()
    clear_background(RAYWHITE)
    
    
    draw_rectangle(0, int(L), 400, 800 - int(L), BLUE)
    
    
    draw_line(0, 525, 400, 525, BLACK)
    
    
    draw_rectangle(200 - 20, int(getScreenY(Y)) - 20, 40, 40, RED)
    
    
    draw_text(str(round(Y, 2)), 10, 10, 20, BLACK)
    draw_text(str(round(M, 2)), 10, 35, 20, BLACK)
    
    end_drawing()

close_window()