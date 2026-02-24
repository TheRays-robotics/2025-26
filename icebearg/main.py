import asyncio
from pyray import *
import os
from math import dist,cos,sin
from math import radians as rad
import colorutils
from haversine import haversine
import re
from time import sleep

def processColor(c,o):
    color = colorutils.hex_to_rgb("#"+c)
    return(Color(color[0],color[1],color[2],o))
X,Y=0,1
def scale(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
def scaleInt(value, istart, istop, ostart, ostop):
    return int(ostart + (ostop - ostart) * ((value - istart) / (istop - istart)))
def getGPos(x,y):
    return(scale(x,0,w,45,49),scale(y,0,h,-47,-49))
def getSpos(x,y):
    return(int(scale(x,45,49,0,w)),int(scale(y,-47,-49,0,h)))

set_trace_log_level(TraceLogLevel.LOG_ERROR) 

class platform:
    def __init__(self, lat, long, depth,name):
        self.x = lat
        self.y = long
        self.depth = depth
        self.name = name
class ice:
    def __init__(self, lat, long,depth,head):
        self.x = lat
        self.y = long
        self.depth = depth
        self.head = head
Hibernia = platform(46.7504,-48.7819,-78,"Hibernia")
SeaRose = platform(46.7895,-48.1417,-107,"SeaRose")
TerraNova = platform(46.4,-48.4,-91,"TerraNova")
Hebron = platform(46.544,-48.498,-93,"Hebron")

platforms = [Hibernia,SeaRose,TerraNova,Hebron]

evil = ice(46,-48,-10,300)

async def main():
    init_window(100, 100, "soup")
    global h
    global w
    h,w = get_monitor_width(get_current_monitor())-900,get_monitor_height(get_current_monitor())-300
    set_window_size(w,h)
    set_window_position(int(h/2),50)

    while not window_should_close():
        clear_background(WHITE)
        
        #print(evil.x,evil.y)
        print(getGPos(get_mouse_x(),get_mouse_y()))
        for P in platforms:
            slat,slong = getSpos(P.x,P.y)
            draw_circle(slat,slong,50,GOLD)
            draw_circle(slat,slong,25,RED)
            draw_circle(slat,slong,10,BLACK)
            GD = haversine((P.x,P.y),(evil.x,evil.y),unit="nmi")
            draw_text(str(round(GD,2))+"NMI",slat,slong-70,30,BLUE)
            #draw_text(str(dist(getSpos(P.x,P.y),getSpos(evil.x,evil.y))),slat-30,slong-120,30,BLUE)
            if check_collision_point_circle(Vector2(get_mouse_x(),get_mouse_y()),(slat,slong),15):
                draw_text("("+str(P.x)+","+str(P.y)+")",slat-30,slong-40,30,BLUE)
            else:
                draw_text(P.name,slat-30,slong-40,30,BLUE)

            slat,slong = getSpos(evil.x,evil.y)
            if slong < get_mouse_y():
                evil.x += cos(rad(evil.head))/1000
                evil.y += sin(rad(evil.head))/1000
            if slong > get_mouse_y():
                evil.x -= cos(rad(evil.head))/1000
                evil.y -= sin(rad(evil.head))/1000
            draw_circle(slat,slong,5,RED)
                

            

        end_drawing()

    close_window()

asyncio.run(main())