import math

def get_dist(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) * ((y1 - y2) ** 2))

def pixels_to_meters(pixel_pos: tuple, pixel_size: tuple):
    x = (pixel_pos[0] - 72.0 * (pixel_size[0] / 1812.0)) * (16.46 / 1668.0) * (1812.0 / pixel_size[0])
    y = (pixel_pos[1] - 49.0 * (pixel_size[1] / 934.0)) * (8.23 / 838.0) * (934.0 / pixel_size[1])
    return x, y

def meters_to_pixels(pos: tuple, pixel_size: tuple):
    x = pos[0] * (pixel_size[0] / 1812.0) * (1668.0 / 16.46) + 72.0 * (pixel_size[0] / 1812.0)
    y = pos[1] * (pixel_size[1] / 934.0) * (838.0 / 8.23) + 49.0 * (pixel_size[1] / 934.0)
    return x, y