import asyncio
from pyray import *
from colorutils import hex_to_rgb
# size:1366,688
def scale(value, istart, istop, ostart, ostop):
	return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
async def main():   # You MUST have an async main function
    init_window(get_screen_width(), get_screen_height(), "Hello")
    while not window_should_close():
        print(get_screen_width(), get_screen_height())
        begin_drawing()
        clear_background(BLACK)
        draw_text("Hello world", 190, get_mouse_y(), int((get_mouse_x()/10)),LIME)
        end_drawing()
        await asyncio.sleep(0) # You MUST call this in your main loop
    close_window()

asyncio.run(main())