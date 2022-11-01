import math

class Point:
    def __init__(self, index: int, delta_time: float, x: float, y: float, angle: float):
        #index in point list
        self.index = index
        #time from previous point
        self.delta_time = delta_time
        #absolute time in path
        self.time = 0.0
        #x and y position in meters
        self.x = x
        self.y = y
        #angle in radians
        self.angle = angle
    
    def set_angle_degrees(self, degrees: float):
        self.angle = degrees * (math.pi / 180.0)

    def get_angle_degrees(self):
        return self.angle * (180.0 / math.pi)

    def to_json(self):
        return self.__dict__