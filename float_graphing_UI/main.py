import asyncio
from pyray import *
import os
from math import dist
import colorutils
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import serial
from time import sleep
global line

ser = serial.Serial('COM6', 115200,timeout=100)
#on chrome run command before main.py: export DISPLAY=:0
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

width,height=1366, 768-45-30

profiles=[[(0,0),(5,1),(10,2),(15,3)],[(0,3),(5,2),(10,1),(15,0)]]
def circleButton(x,y,radius,image,color):
    draw_circle(x,y,radius,color)
    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
        if dist((get_mouse_x(),get_mouse_y()),(x,y)) <= radius:
            return(True)
    return(False)
    
mainfont = "mononoki-Regular.ttf"
async def main():
    init_window(width, height, "soup")
    current_profile = 0
    line=""
    while not window_should_close():
        font = load_font_ex(("float_graphing_UI/"+mainfont).encode(),30,None,0)
        begin_drawing()
        clear_background(BLACK)
        #draw_text("Hello world", 190, get_mouse_y(), int((get_mouse_x()/10)), LIME)
        if circleButton(789,135,25,NotImplemented,R_GREEN):
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
        draw_line(0,36,width,36,WHITE)
        draw_line(36,36,36,height,WHITE)
        draw_line(660,36,660,height,WHITE)
        draw_text(str(profiles[current_profile]),500,100,10,R_GREEN)
        for i in range(len(profiles)):
                    draw_rectangle(0,37+(36*i),35,36,(W_PURPLE,W_PURPLE2)[i%2])
                    draw_text_ex(font,str(i+1),Vector2(10,42+(36*i)),25,2,WHITE)
        if get_mouse_x() <= 36:
                    for i in range (len(profiles)):
                        if get_mouse_y() > 37+(36*i) and get_mouse_y() < 36+37+(36*i):
                            draw_rectangle_lines(0,37+(36*i),35,36,WHITE)
                            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
                                draw_rectangle(0,37+(36*i),35,36,WHITE)
                                print(i)
                                current_profile = i
        
        draw_line(36,72,658,72,WHITE)
        draw_line(348,72,348,height,WHITE)
        
        if circleButton(500,200,60,NotImplemented,W_PURPLE2):
            ser.write(bytes('AT+SEND=27,1,D\r\n',"utf-8"))

        for point in profiles[current_profile]:
            I = profiles[current_profile].index(point)
            draw_text_ex(font,str(point[Y])+"(s)",Vector2(350,I*30+72),20,2,WHITE)
            draw_text_ex(font,str(point[X])+"(m)",Vector2(40,I*30+72),20,2,WHITE)
            draw_line(36,I*30+94,658,I*30+94,WHITE)
        draw_fps(300,0)
        if ser.in_waiting > 0:
            line = str(ser.readline().decode(encoding="utf-8")).replace('\n',"")
            if "*" in line:
                profiles[-1].append([float(re.findall(r"T.*|",line)[-1].replace("T","0")),float(re.findall(r"|.*P",line)[-1].replace("W","0"))])
            if "stop" in line:
                 profiles.append([])

        end_drawing()

    close_window()

asyncio.run(main())