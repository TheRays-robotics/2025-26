import asyncio
from pyray import *
import os
from math import dist
X,Y=0,1
def scale(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

width,height=get_screen_width(), get_screen_height()
def circleButton(x,y,radius,image,color):
    draw_circle(x,y,radius,color)
    if is_mouse_button_pressed(is_mouse_button_pressed(1)):
        if dist((get_mouse_x(),get_mouse_y()),(x,y)) <= radius:
            return(True)
    return(False)
    
mainfont = "mononoki-Regular.ttf"

async def graph(data):
    init_window(width, height, "hi")
    font = load_font_ex(("float_graphing_UI/"+mainfont).encode(),300,None,0)
    should_exit = False
    highests = (0,0)
    lowests = (0,0)
    for point in data:
        if point[X] > highests[X]:
            highests[X] = point[X]
    for point in data:
        if point[Y] > highests[Y]:
            highests[Y] = point[Y]
    for point in data:
        if point[X] > lowests[X]:
            lowests[X] = point[X]
    for point in data:
        if point[Y] > lowests[Y]:
            lowests[Y] = point[Y]

    for point in data:
        draw_circle(scale(point[X],lowests[X],highests[X],33,1360),scale(point[X],lowests[X],highests[X],0,175))
    
    while not window_should_close() and not should_exit:
        begin_drawing()
        clear_background(BLACK)
        #draw_text_ex(font, "Hey Kitten", Vector2(190, get_mouse_y()), int(get_mouse_x()/10) ,int(get_mouse_x()/50), BLUE)
        end_drawing()
        
        if is_key_pressed(KeyboardKey.KEY_ESCAPE):
            should_exit = True
        
        await asyncio.sleep(0)
    
    

    close_window()

async def main():
    current_state = "main_window"
    while current_state != "quit":
        if current_state == "main_window":
        
            init_window(width, height, "MAIN")
            while not window_should_close():
                begin_drawing()
                clear_background(BLACK)
                #draw_text("Hello world", 190, get_mouse_y(), int((get_mouse_x()/10)), LIME)
                if circleButton(789,135,25,NotImplemented,BLUE):
                    break
                





                end_drawing()
                await asyncio.sleep(0)
            
        
            if window_should_close():
                current_state = "quit"
            else:
                close_window()
                current_state = "graph_window"
                
        elif current_state == "graph_window":
            await graph([(0,0),(5,10),(10,5),(15,15)])
            current_state = "main_window"
    

    close_window()

asyncio.run(main())