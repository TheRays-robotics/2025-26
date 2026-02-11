import asyncio
from pyray import *
import os
from math import dist
import colorutils
import haversine
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
    return(scale(x,0,w,42,50),scale(y,0,h,-47,-49))
def getSpos(x,y):
    return(int(scale(x,42,50,0,w)),int(scale(y,-47,-49,0,h)))

set_trace_log_level(TraceLogLevel.LOG_ERROR) 

class platform:
    def __init__(self, lat, long, depth,name):
        self.x = lat
        self.y = long
        self.depth = depth
        self.name = name
Hibernia = platform(43.7504,-48.7819,-78,"Hibernia")
SeaRose = platform(46.7895,-48.1417,-107,"SeaRose")
TerraNova = platform(46.4,-48.4,-91,"TerraNova")
Hebron = platform(46.544,-48.498,-93,"Hebron")

platforms = [Hibernia,SeaRose,TerraNova,Hebron]

async def main():
    init_window(100, 100, "soup")
    global h
    global w
    h,w = get_monitor_width(get_current_monitor())-900,get_monitor_height(get_current_monitor())-300
    set_window_size(w,h)
    set_window_position(int(h/2),50)

    while not window_should_close():
        clear_background(BLACK)

        for P in platforms:
            slat,slong = getSpos(P.x,P.y)
            print(slat,slong)
            draw_circle(slat,slong,10,WHITE)
            if dist()

        end_drawing()

    close_window()

asyncio.run(main())