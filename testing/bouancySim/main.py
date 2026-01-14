from pyray import *
import serial
import re
from time import time
init_window(400, 800, "goob")
set_target_fps(60)
doserial = False
if doserial:    
    ser = serial.Serial('COM5', 9600,timeout=10)
def getScreenY(y):
    return((y*170)+L)
#170pixels = 1M
L = 100
G = 9.8
S = 9.8+3.7765
M = 0
Y = -1
V = 0.0
sub = 0

set_trace_log_level(TraceLogLevel.LOG_ERROR) 
start=time()
while not window_should_close():
    #L=get_mouse_y()
    if doserial:
        ser.write((str(int(Y*100)/100)+"\n").encode())
        if ser.in_waiting > 0:
            LINE=ser.readline().decode(encoding="utf-8")
            print(LINE)
            M=((float(LINE)/180)*300)
    #print(Y)
    dt = get_frame_time()
    V += G * dt
    if int(getScreenY(Y)) > 0:
        sub = max(0, min(1.0, (getScreenY(Y) + 20 - L) / 40.0))
        
        print(sub)
        V -= (S) * sub * dt
        V *= 1-(sub*0.05)

    Y += V * dt
    if Y > 4:
        Y = 4
        V *= -0.5
    begin_drawing()
    clear_background(RAYWHITE)
    draw_rectangle(0, int(L), 800, 800-int(L), BLUE)
    draw_line(0,525,400,525,BLACK)
    draw_rectangle(200-20, int(getScreenY(Y))-20, 40, 40, RED)
    draw_text(str(int(Y*100)/100), 200-20, int(Y)-10 ,20 ,BLACK)
    end_drawing()

close_window()