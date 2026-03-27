import asyncio
from pyray import *
from math import cos, sin, radians as rad
from haversine import haversine

crabs = [["Snow crab (chionecetes opilio)",0],
["Acadian hermit crab (Pagarus acadianus)",9],
["Western Atlantic Hairy Hermit Crab (Pagarus arcuatus)",0],
["European Green Crab (Carcinus maenas)",0],
["Rock Crab (Cancer pagurus)",0],
["Jonah Crab (Cancer borealis)",0],
["Spiny Sunstar (Crossaster papposus)",1],
["Sea Urchin (Stronglyocentrotus droebachiensis)",0],
["Boreal Sea Star (Boreal asterias)",0],
["Daisy brittle star (Ophiopholis aculeata)",0]]

sum = 0
for C in crabs:
    n = int(input(C[0]))
    C[1] = n
    sum+=n
print(sum)

for C in crabs:
    n = C[1]
    C[1] = str((n/sum)*100)+"%"


async def main():
    init_window(100, 100, "soup")
    set_trace_log_level(TraceLogLevel.LOG_ERROR)
    set_window_size(1200, 600)
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)
        i = 0
        draw_line(1000,0,1000,1000,BLUE)
        for C in crabs:
            draw_line(0,50+(i*50),2000,50+(i*50),BLUE)
            draw_text(C[0],10,60+(i*50),30,BLACK)
            draw_text(C[1],1030,60+(i*50),30,BLACK)
            
            i+=1
        draw_line(0,50+(i*50),2000,50+(i*50),BLUE)
        end_drawing()
    close_window()

asyncio.run(main())
