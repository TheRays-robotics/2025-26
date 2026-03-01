import asyncio
from pyray import *
from math import cos, sin, radians as rad
from haversine import haversine

def scale(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def getSpos(lat, lon, w, h):
    sx = scale(lon, -49.5, -47.5, 0, w)
    sy = scale(lat, 45.5, 47.5, h, 0)+400
    return int(sx), int(sy)

class platform:
    def __init__(self, lat, long, depth, name):
        self.lat = lat
        self.lon = long
        self.depth = depth
        self.name = name

class ice:
    def __init__(self, lat, long, depth, head):
        self.lat = lat
        self.lon = long
        self.depth = depth
        self.head = head

Hibernia = platform(46.7504, -48.7819, -78, "Hibernia")
SeaRose = platform(46.7895, -48.1417, -107, "SeaRose")
TerraNova = platform(46.4, -48.4, -91, "TerraNova")
Hebron = platform(46.544, -48.498, -93, "Hebron")

platforms = [Hibernia, SeaRose, TerraNova, Hebron]
evil = ice(46.2, -48.2, -80, 310)

async def main():
    init_window(100, 100, "soup")
    set_trace_log_level(TraceLogLevel.LOG_ERROR)
    w = get_monitor_width(get_current_monitor()) - 900
    h = get_monitor_height(get_current_monitor()) - 300
    set_window_size(w, h)
    set_window_position(int(w/3),40)
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)

        slon_ice, slat_ice = getSpos(evil.lat, evil.lon, w, h)
        
        # FIXED SCALING
        # Latitude: 2.0 deg = 120 NMI. Longitude at 46N: 2.0 deg = ~83.4 NMI
        ppn_y = h / 120.0
        ppn_x = w / 83.4 
        
        evildirlat = cos(rad(evil.head)) * 0.0005
        evildirlon = sin(rad(evil.head)) * 0.0005

        if slat_ice < get_mouse_y():
            evil.lat -= evildirlat
            evil.lon -= evildirlon
        elif slat_ice > get_mouse_y():
            evil.lat += evildirlat
            evil.lon += evildirlon

        for P in platforms:
            sx, sy = getSpos(P.lat, P.lon, w, h)
            GD = haversine((P.lat, P.lon), (evil.lat, evil.lon), unit="nmi")
            
            # Draw as Ellipses to account for Longitude distortion
            draw_ellipse_lines(sx, sy, 10 * ppn_x, 10 * ppn_y, GOLD)
            draw_ellipse_lines(sx, sy, 5 * ppn_x, 5 * ppn_y, RED)
            draw_circle(sx, sy, 5, BLACK)
            
            draw_text(str(round(GD, 2)) + "NMI", sx - 20, sy - 60, 25, BLUE)

            if check_collision_point_circle(Vector2(get_mouse_x(), get_mouse_y()), (sx, sy), 15):
                draw_text(f"({P.lat}, {P.lon})", sx - 30, sy + 20, 20, BLUE)
            else:
                draw_text(P.name, sx - 30, sy + 20, 20, BLUE)

            ind = platforms.index(P)

            draw_rectangle(100, 100 + (100 * ind),1000,int((100*(len(platforms)-2))/2),GREEN)
            if GD < 10:
                if GD < 5:
                    draw_rectangle(100, 100 + (100 * ind),500,100, RED)
                else:
                    draw_rectangle(100, 100 + (100 * ind),500,100, YELLOW)
            if 0.9 < evil.depth/P.depth < 1.1:
                draw_rectangle(600, 100 + (100 * ind),500,100, RED)
            if 0.7 < evil.depth/P.depth < 0.9:
                draw_rectangle(600, 100 + (100 * ind),500,100, YELLOW)
            draw_text(str(P.name), 130, 130 + (100 * ind), 50, BLACK)
            draw_text(str(P.name), 630, 130 + (100 * ind), 50, BLACK)
            draw_line(100, 100 + (100 * ind), 1100, 100 + (100 * ind), BLACK)
            draw_line(100, 100 + (100 * (ind + 1)), 1100, 100 + (100 * (ind + 1)), BLACK)

        draw_line(100, (100 * len(platforms)) + 100, 100, 100, MAGENTA)
        draw_line(1100, (100 * len(platforms)) + 100, 1100, 100, MAGENTA)
        draw_line(600, (100 * len(platforms)) + 100, 600, 100, MAGENTA)

        draw_circle(slon_ice, slat_ice, 8, SKYBLUE)
        
        draw_text("Threat to platforms", 130, 50, 30, BLACK)
        draw_text("Threat to undersea assets", 630, 50, 30, BLACK)

        end_drawing()
    close_window()

asyncio.run(main())
