import asyncio
from pyray import *
def scale(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

width,height=get_screen_width(), get_screen_height()

async def second():
    """Logic for the second window."""
    init_window(width, height, "hi")
    should_exit = False
    
    while not window_should_close() and not should_exit:
        begin_drawing()
        clear_background(BLACK)
        draw_text("Hello world", 190, get_mouse_y(), int((get_mouse_x()/10)), BLUE)
        end_drawing()
        
        if is_key_pressed(KeyboardKey.KEY_ESCAPE):
            should_exit = True
        
        await asyncio.sleep(0)
    

    close_window()

async def main():
    """Main loop for handling window switching."""
    current_state = "main_window"
    
    while current_state != "quit":
        if current_state == "main_window":
        
            init_window(width, height, "Hello")
            while not window_should_close():
                begin_drawing()
                clear_background(BLACK)
                draw_text("Hello world", 190, get_mouse_y(), int((get_mouse_x()/10)), LIME)
                
            
                if is_key_pressed(KeyboardKey.KEY_SPACE):
                    break
                
                end_drawing()
                await asyncio.sleep(0)
            
        
            if window_should_close():
                current_state = "quit"
            else:
                close_window()
                current_state = "second_window"
                
        elif current_state == "second_window":
            await second()
            current_state = "main_window"
    

    close_window()

asyncio.run(main())