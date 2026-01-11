from pyray import *
import serial
import re
from time import time
init_window(400, 800, "goob")
set_target_fps(60)
doserial = False
if doserial:    
    ser = serial.Serial('COM5', 9600,timeout=10)
L = 100
G = 1013.0 #9.8 m/s^2
S = 1013.0 +255.040719353
M = 0
Y = 0
V = 0.0
sub = 0
RM = 0
set_trace_log_level(TraceLogLevel.LOG_ERROR) 
start=time()
SH = ((L-Y)/680)*4
while not window_should_close():
    if abs(time()-start - 1) < 0.01:
        print((((L-Y)/680)*4)-SH)
        pass
    if doserial:
        ser.write((str(int((((L-Y)/680)*4)*100)/100)+"\n").encode())
        if ser.in_waiting > 0:
            LINE=ser.readline().decode(encoding="utf-8")
            print(LINE)
            RM=((float(LINE)/180)*300)
    dt = get_frame_time()
    V += G * (RM+1) * dt
    if Y + 20 > L:
        sub = min(1.0, (Y + 20 - L) / 40.0)
        
        V -= (S) * sub * dt
        V *= 0.95
        #V -= (432.578909185*(V*V))
        
    Y += V * dt
    if Y > 780:
        Y = 780
        V *= -0.5
    
    begin_drawing()
    clear_background(RAYWHITE)
    draw_rectangle(0, int(L), 800, 800-int(L), BLUE)
    draw_line(0,525,400,525,BLACK)
    draw_rectangle(200-20, int(Y)-20, 40, 40, RED)
    draw_text(str(int((((Y-L)/680)*4)*100)/100), 200-20, int(Y)-10 ,20 ,BLACK)
    end_drawing()

close_window()