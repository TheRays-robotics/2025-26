from pyray import *
import serial
from time import time,sleep
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
    ser = serial.Serial('COM5', 9600, timeout=10)

def getScreenY(y):
    return ((y * 170) + L)

L = 100  
G = 9.8  
S = 9.8+3.7765 
M = 6.8
sm = M
Y = 0
V = 0 
EM = 0
sub = 0
PM=0
pidvals=""
set_trace_log_level(TraceLogLevel.LOG_ERROR) 
mainfont = "mononoki-Regular.ttf"
while not window_should_close():
    font = load_font_ex((mainfont).encode(),30,None,0)
    if doserial:
        #print((str(Y) + "\n").encode())
        ser.write((str(Y) + "\n").encode())
        if ser.in_waiting > 0:
            LINE = ser.readline().decode(encoding="utf-8")
            print(LINE)
            if LINE[0] == "M":
                LINE = LINE.strip("M")
                M = sm + ((float(LINE) / 180) * 11) + EM
            if LINE[0] == "P":
                pidvals = LINE.strip("P")
    else:
        M = sm + EM
    dt = get_frame_time()
    if is_mouse_button_pressed(0):
        EM += 1
    if is_mouse_button_pressed(1):
        EM -= 1
    screen_y = getScreenY(Y)
    total_force = M * G
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
    draw_rectangle(200 - 20, int(getScreenY(Y)) - 20, 40, 40, RED)
    #draw_texture(texture,200 - 20, int(getScreenY(Y))-20,WHITE)
    draw_text_ex(font,pidvals,Vector2(0,0), 20, 2,BLACK)
    draw_text_ex(font,str(round(Y, 2)), Vector2(180, getScreenY(Y)-20), 20, 2,BLACK)
    draw_text_ex(font,str(round(M, 2)), Vector2(10, 35), 20,2, BLACK)
    draw_text_ex(font,str(round((((M-sm)/11)*100),3))+"%", Vector2(10, 60), 20, 2, BLACK)

    end_drawing()

close_window()
sleep(2)