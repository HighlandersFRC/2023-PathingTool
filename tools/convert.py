import math
import pyautogui

#height of the windows taskbar, in pixels
TASK_BAR_HEIGHT = 40

#vertical resolution of the screen
VERTICAL_RESOLUTION = 900

def get_dist(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

def pixels_to_meters(pixel_pos: tuple, pixel_size: tuple):
    x = (pixel_pos[0] - 72.0 * (pixel_size[0] / 1812.0)) * (16.46 / 1668.0) * (1812.0 / pixel_size[0])
    y = (pixel_pos[1] - 49.0 * (pixel_size[1] / 934.0)) * (8.23 / 838.0) * (934.0 / pixel_size[1])
    return x, y

def meters_to_pixels(pos: tuple, pixel_size: tuple):
    x = pos[0] * (pixel_size[0] / 1812.0) * (1668.0 / 16.46) + 72.0 * (pixel_size[0] / 1812.0)
    y = pos[1] * (pixel_size[1] / 934.0) * (838.0 / 8.23) + 49.0 * (pixel_size[1] / 934.0)
    return x, y

def pixels_to_meters_x(px, pixel_size: tuple):
    return (px - 72.0 * (pixel_size[0] / 1812.0)) * (16.46 / 1668.0) * (1812.0 / pixel_size[0])

def pixels_to_meters_y(py, pixel_size: tuple):
    return (py - 49.0 * (pixel_size[1] / 934.0)) * (8.23 / 838.0) * (934.0 / pixel_size[1])

def meters_to_pixels_x(x, pixel_size: tuple):
    return x * (pixel_size[0] / 1812.0) * (1668.0 / 16.46) + 72.0 * (pixel_size[0] / 1812.0)

def meters_to_pixels_y(y, pixel_size: tuple):
    return y * (pixel_size[1] / 934.0) * (838.0 / 8.23) + 49.0 * (pixel_size[1] / 934.0)

def get_robot_radius(robot_width: float, robot_height: float):
    return math.sqrt((robot_width / 2.0) ** 2 + (robot_height / 2.0) ** 2)

def sum_lists(l1: list[float], l2: list[float]):
    ret = []
    for i in range(min(len(l1), len(l2))):
        ret.append(l1[i] + l2[i])
    return ret

def get_cursor_dist_meters(selected_pos_meters: list[float], pixel_size: list[float]):
    x, y = pyautogui.position()
    y = VERTICAL_RESOLUTION - y - TASK_BAR_HEIGHT
    cursor_pos_meters = pixels_to_meters((x, y), pixel_size)
    return get_dist(cursor_pos_meters[0], cursor_pos_meters[1], selected_pos_meters[0], selected_pos_meters[1])

def get_cursor_pos_meters(pixel_size: list[float]):
    x, y = pyautogui.position()

    y = VERTICAL_RESOLUTION - y - TASK_BAR_HEIGHT
    return pixels_to_meters((x, y), pixel_size)