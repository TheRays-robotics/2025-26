import asyncio
from pyray import *
import os
from math import dist
#run command before file: export DISPLAY=:0
X,Y=0,1
def scale(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
def scaleInt(value, istart, istop, ostart, ostop):
    return int(ostart + (ostop - ostart) * ((value - istart) / (istop - istart)))
R_GREEN = Color(89, 208, 55,255)
width,height=1366, 768-45-30

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
                if circleButton(789,135,25,NotImplemented,R_GREEN):
                    break
                





                end_drawing()
                await asyncio.sleep(0)
            
        
            if window_should_close():
                current_state = "quit"
            else:
                close_window()
                current_state = "graph_window"
                
        elif current_state == "graph_window":
            await graph([(0,0),(5,1),(10,2),(15,3)])
            current_state = "main_window"
    

    close_window()

asyncio.run(main())