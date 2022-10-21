import math

def get_dist(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) * ((y1 - y2) ** 2))

def pixel_to_meters(pixel_pos: tuple):
    return pixel_pos[0] / 100, pixel_pos[1] / 100

def meters_to_pixels(pos: tuple):
    return pos[0] * 100, pos[1] * 100