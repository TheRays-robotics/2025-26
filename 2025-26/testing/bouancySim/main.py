from pyray import *
import serial
import os


base_path = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(base_path, "float.png")

init_window(400, 800, "FLOAT SIM")
set_target_fps(60)


texture = None
if os.path.exists(img_path):
    image = load_image(img_path)
    texture = load_texture_from_image(image)
    unload_image(image)

doserial = True

ser = serial.Serial('COM6', 9600, timeout=5, write_timeout=0) 


L, G, S, M = 100, 9.8, 11.2, 6.8
sm = M
Y, V, EM = 0, 0, 0

while not window_should_close():
    
    if doserial and ser.in_waiting > 0:
        try:
            line = ser.readline().decode().strip()
            print(line)
            if "D" in line:
                M = sm + ((float(line.replace("D","")) / 180) * 5) + EM
            
        except: pass

    
    dt = get_frame_time()
    if is_mouse_button_pressed(0): EM += 1
    if is_mouse_button_pressed(1): EM -= 1
    
    screen_y = (Y * 170) + L
    total_force = M * G
    
    if screen_y + 20 > L:
        sub = max(0, min(1.0, (screen_y + 20 - L) / 40.0))
        total_force -= (S * sub * 10) 
        V *= 1 - (sub * 0.05)

    V += (total_force / M) * dt
    Y += V * dt
    if Y > 4: Y, V = 4, V * -0.1

    
    begin_drawing()
    clear_background(RAYWHITE)
    
    draw_rectangle(0, L, 400, 800 - L, BLUE)
    draw_line(0, 525, 400, 525, BLACK)
    draw_rectangle(180, int(screen_y) - 20, 40, 40, RED)
    
    
    draw_text(f"Y: {round(Y, 2)}", 180, int(screen_y) - 40, 20, BLACK)
    draw_text(f"Mass: {round(M, 2)}", 10, 10, 20, BLACK)

    end_drawing()

    if doserial:
        ser.write((str(Y)+"\n").encode("utf-8"))

close_window()