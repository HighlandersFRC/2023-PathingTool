import math

def get_dist(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) * ((y1 - y2) ** 2))

def pixels_to_meters(pixel_pos: tuple, pixel_size: tuple):
    x = (pixel_pos[0] - 72 * (pixel_size[0] / 1812)) * (16.46 / 1668) * (1812 / pixel_size[0])
    y = (pixel_pos[1] - 49 * (pixel_size[1] / 934)) * (8.23 / 838) * (934 / pixel_size[1])
    return x, y

def meters_to_pixels(pos: tuple, pixel_size: tuple):
    x = pos[0] * (pixel_size[0] / 1812) * (1668 / 16.46) + 72 * (pixel_size[0] / 1812)
    y = pos[1] * (pixel_size[1] / 934) * (838 / 8.23) + 49 * (pixel_size[1] / 934)
    return x, y