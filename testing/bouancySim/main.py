from pyray import *

# Initialization
init_window(800, 600, "Raylib Buoyancy Simulation")
set_target_fps(60)

L = 100
G = 500.0
S = 0.0  # Must be > G for floating
pos = Vector2(400, 0)
V = 0.0
set_trace_log_level(TraceLogLevel.LOG_ERROR) 

while not window_should_close():
    dt = get_frame_time()
    V += G * dt
    if pos.y + 20 > L:
        sub = min(1.0, (pos.y + 20 - L) / 40.0)
        V -= S * sub * dt
        V *= 0.95
        
    pos.y += V * dt
    print(pos.y-100)
    begin_drawing()
    clear_background(RAYWHITE)
    draw_rectangle(0, L, 800, 800-L, BLUE)
    draw_rectangle_v(pos, Vector2(40, 40), RED)
    end_drawing()

close_window()