from pyray import *

# Initialization
init_window(400, 800, "Raylib Buoyancy Simulation")
set_target_fps(60)

L = 100
G = 500.0
S = 700.0  # Must be > G for floating
W = 400
Y=0
V = 0.0
set_trace_log_level(TraceLogLevel.LOG_ERROR) 

while not window_should_close():
    dt = get_frame_time()
    V += G * dt
    if Y + 20 > L:
        sub = min(1.0, (Y + 20 - L) / 40.0)
        V -= (S-W) * sub * dt
        V *= 0.95
        
    Y += V * dt
    if Y > 780:
        Y = 780
        V = 0
    print(int((((Y-100)/680)*4)*100)/100)
    
    begin_drawing()
    clear_background(RAYWHITE)
    draw_rectangle(0, L, 800, 800-L, BLUE)
    draw_line(0,525,400,525,BLACK)
    draw_rectangle(200-20, int(Y)-20, 40, 40, RED)
    end_drawing()

close_window()