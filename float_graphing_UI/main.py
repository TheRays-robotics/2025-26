import asyncio
from pyray import *
import os
from math import dist
import colorutils
#run command before main.py: export DISPLAY=:0
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
async def graph(data):
    init_window(width, height, "hi")
    font = load_font_ex(("float_graphing_UI/"+mainfont).encode(),300,None,0)
    should_exit = False
    highests = [0,0]
    lowests = [1000000,100000]
    for point in data:
        if point[X] > highests[X]:
            highests[X] = point[X]
    for point in data:
        if point[Y] > highests[Y]:
            highests[Y] = point[Y]
    for point in data:
        if point[X] < lowests[X]:
            lowests[X] = point[X]
    for point in data:
        if point[Y] < lowests[Y]:
            lowests[Y] = point[Y]

       
    while not window_should_close() and not should_exit:
        begin_drawing()
        clear_background(Color(20,50,20))
        draw_rectangle(33,0,width-33,height-33,(BLACK))

        #Y AXIS LABELS
        verticalmarkerdistance = scale(0.5,lowests[Y],highests[Y],0,height-33)
        for i in range(int(highests[Y]/0.5)):
            draw_line(0,int(verticalmarkerdistance*i),width,int(verticalmarkerdistance*i),WHITE)
            draw_text_ex(font,str(i*0.5),Vector2(0,int(verticalmarkerdistance)*i),15,2,R_GREEN)
        draw_text_ex(font,str(highests[Y]),Vector2(0,height-33),15,2,R_GREEN)
        draw_line(0,height-33,width,height-33,WHITE)

        #X AXIS LABELS
        horizontalmarkerdistance = scale(5,lowests[X],highests[X],0,width-33)
        for i in range(int(highests[X]/5)):
            draw_line(int(horizontalmarkerdistance*i)+33,0,int(horizontalmarkerdistance*i)+33,height-33,WHITE)
            draw_text_ex(font,str(i*5),Vector2(int(horizontalmarkerdistance*i)+33,height-33),15,2,R_GREEN)
        draw_text_ex(font,str(highests[X]),Vector2(width,height-33),15,2,R_GREEN)
        draw_line(width,height-33,width,0,WHITE)

        for point in data:
            #draw_line(0,scaleInt(point[Y],lowests[Y],highests[Y],0,height-33),width,scaleInt(point[Y],lowests[Y],highests[Y],0,height-33),WHITE)
            
            draw_circle(int(scale(point[X],lowests[X],highests[X],33,width)),int(scale(point[Y],lowests[Y],highests[Y],0,height-33)),8,BLACK)
            draw_circle(int(scale(point[X],lowests[X],highests[X],33,width)),int(scale(point[Y],lowests[Y],highests[Y],0,height-33)),7,R_GREEN)
            draw_text(str(point),int(scale(point[X],lowests[X],highests[X],33,width)),int(scale(point[Y],lowests[Y],highests[Y],0,height-33)),10,RED)
            
            #draw_text_ex(font,str(point[Y]),Vector2(0,scale(point[Y],lowests[Y],highests[Y],0,height-33)),15,2,R_GREEN)
        end_drawing()
        
        if is_key_pressed(KeyboardKey.KEY_ESCAPE):
            should_exit = True
        
        await asyncio.sleep(0)
    
    

    close_window()

async def main():
    current_state = "main_window"
    while current_state != "quit":
        if current_state == "main_window":
            current_profile = 0
            init_window(width, height, "MAIN")
            font = load_font_ex(("float_graphing_UI/"+mainfont).encode(),30,None,0)
            while not window_should_close():
                begin_drawing()
                clear_background(BLACK)
                #draw_text("Hello world", 190, get_mouse_y(), int((get_mouse_x()/10)), LIME)
                if circleButton(789,135,25,NotImplemented,R_GREEN):
                    break
                draw_line(0,36,width,36,WHITE)
                draw_line(36,36,36,height,WHITE)
                draw_line(660,36,660,height,WHITE)
                for i in range(len(profiles)):
                    draw_rectangle(0,37+(36*i),35,36,(W_PURPLE,W_PURPLE2)[i%2])
                    draw_text_ex(font,str(i+1),Vector2(10,42+(36*i)),25,2,WHITE)
                if get_mouse_x() <= 36:
                    for i in range (len(profiles)):
                        if get_mouse_y() > 37+(36*i) and get_mouse_y() < 36+37+(36*i):
                            draw_rectangle_lines(0,37+(36*i),35,36,WHITE)
                            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                                draw_rectangle(0,37+(36*i),35,36,WHITE)
                                current_profile = i
                
                draw_line(36,72,658,72,WHITE)
                draw_line(348,72,348,height,WHITE)
                for point in profiles[current_profile]:
                    I = profiles[current_profile].index(point)
                    draw_text_ex(font,str(point[Y])+"(s)",Vector2(350,I*30+72),20,2,WHITE)
                    draw_text_ex(font,str(point[X])+"(m)",Vector2(40,I*30+72),20,2,WHITE)
                    draw_line(36,I*30+94,658,I*30+94,WHITE)
                draw_fps(300,0)

                end_drawing()
                await asyncio.sleep(0)
            
        
            if window_should_close():
                current_state = "quit"
            else:
                close_window()
                current_state = "graph_window"
                
        elif current_state == "graph_window":
            await graph(profiles[current_profile])
            current_state = "main_window"
    

    close_window()

asyncio.run(main())