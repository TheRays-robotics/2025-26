import asyncio
from pyray import *
import os
from math import dist
import colorutils
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import serial
import re
from time import sleep

global line
global expectedIndex
try:
    ser = serial.Serial('COM7', 115200,timeout=100)
    DoSerial = True
except:
    DoSerial = False
def processColor(c,o):
    color = colorutils.hex_to_rgb("#"+c)
    return(Color(color[0],color[1],color[2],o))
X,Y=0,1
def scale(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
def scaleInt(value, istart, istop, ostart, ostop):
    return int(ostart + (ostop - ostart) * ((value - istart) / (istop - istart)))
R_GREEN = processColor("3FCC2C",255)
W_PURPLE = processColor("4E008E",255)
W_PURPLE2 = processColor("7F2C92",255)
set_trace_log_level(TraceLogLevel.LOG_ERROR) 
width,height=2000, 1000
#1506, 768-45-30
global nfds
nfds = []
profiles=[[]]
def circleButton(x,y,radius,image,color,strcol):
    img = load_texture(str(os.path.relpath(__file__).replace("main.py",image+".png")))
    draw_circle(x,y,radius,color)
    draw_texture(img,x-radius,y-radius,WHITE)
    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
        if dist((get_mouse_x(),get_mouse_y()),(x,y)) <= radius:
            nfds.append(["draw_circle("+str(x)+","+str(y)+","+str(radius+5)+","+strcol+")",500])
            return(True)
    return(False)
    
mainfont = str(os.path.relpath(__file__).replace("main.py","mononoki-Regular.ttf"))
async def main():
    init_window(width, height, "soup")
    current_profile = 0
    line=""
    font = load_font_ex((mainfont).encode(),30,None,0)
    while not window_should_close():
        begin_drawing()
        clear_background(BLACK)
        for I in nfds:
            exec(I[0])
            if I[1] > 0:
                  I[1] -= 1
            if I[1] == 0:
                 nfds.remove(I)

        if circleButton(1060,140,50,"GRAPHBUTTON",R_GREEN,"R_GREEN"):
            x_values = []
            y_values = []
            for p in profiles[current_profile]:
                x_values.append(p[X])
                y_values.append(p[Y])
            plt.plot(x_values, y_values)
            plt.xlabel("Time (s)")
            plt.ylabel("Depth (m)")
            plt.title("Profile : "+str(current_profile+1))
            plt.show()
        draw_line(0,50,width,50,WHITE)
        draw_line(50,50,50,height,WHITE)
        draw_line(924,50,924,height,WHITE)
        for i in range(len(profiles)):
                    draw_rectangle(0,51+(50*i),49,50,(W_PURPLE,W_PURPLE2)[i%2])
                    draw_text_ex(font,str(i+1),Vector2(10,55+(50*i)),40,2,WHITE)
        if get_mouse_x() <= 50:
                    for i in range (len(profiles)):
                        if get_mouse_y() > 51+(50*i) and get_mouse_y() < 50+51+(50*i):
                            draw_rectangle_lines(0,51+(50*i),60,50,WHITE)
                            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
                                draw_rectangle(0,51+(50*i),35,50,WHITE)
                                current_profile = i
        
        draw_line(50,100,921,100,WHITE)
        draw_line(487,100,487,height,WHITE)
        
        if circleButton(1200,140,50,"DIVEBUTTON",W_PURPLE2,"W_PURPLE2"):
            print("D")
            ser.write(bytes('AT+SEND=27,1,D\r\n',"utf-8"))
            ser.write(bytes('AT+SEND=27,1,n\r\n',"utf-8"))

            print("D")

        for point in profiles[current_profile]:
            I = profiles[current_profile].index(point)
            draw_text_ex(font,str(point[Y])+"(m)",Vector2(486,I*30+100),20,2,WHITE)
            draw_text_ex(font,str(point[X])+"(s)",Vector2(55,I*30+100),20,2,WHITE)
            draw_line(50,I*30+94,921,I*30+94,WHITE)
        draw_fps(300,0)
        if DoSerial:
            if ser.in_waiting > 0:
                line = str(ser.readline().decode(encoding="utf-8")).replace('\n',"")
                print(line)
                if "N" in line:
                    print(int(re.findall(r"N.*N",line)[-1].strip("N")),len(profiles[-1]))
                    if int(re.findall(r"N.*N",line)[-1].strip("N")) == len(profiles[-1]):
                        ser.write(bytes('AT+SEND=27,1,n\r\n',"utf-8"))
                if "TP" in line:
                    profiles[-1].append([float(re.findall(r"T.*T",line)[-1].strip("T")),
                                        float(re.findall(r"P.*P",line)[-1].strip("P"))*-1])
                if "stop" in line:
                    profiles.append([])
                    ser.write(bytes('AT+SEND=27,1,n\r\n',"utf-8"))


        end_drawing()

    close_window()

asyncio.run(main())