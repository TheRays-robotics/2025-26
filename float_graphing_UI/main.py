import asyncio
from pyray import *
from colorutils import hex_to_rgb as col

async def main():   # You MUST have an async main function
    init_window(get_screen_width(), get_screen_height(), "Hello")
    while not window_should_close():
        begin_drawing()
        clear_background(col("000000"))
        draw_text("Hello world", 190, 200, 20, VIOLET)
        end_drawing()
        await asyncio.sleep(0) # You MUST call this in your main loop
    close_window()

asyncio.run(main())