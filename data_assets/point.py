import math

class Point:
    def __init__(self, index: int, x: float, y: float, angle: float):
        #index in point list
        self.index = index
        #x and y position in meters
        self.x = x
        self.y = y
        #angle in radians
        self.angle = angle
    
    def set_angle_degrees(self, degrees: float):
        self.angle = degrees * (math.pi / 180.0)

    def get_angle_degrees(self):
        return self.angle * (180.0 / math.pi)