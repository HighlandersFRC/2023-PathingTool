from kivy.uix.image import Image
from kivy.graphics import *

from data_assets.point import Point
from tools import convert

class Path(Image):
    def __init__(self, **kwargs):
        super().__init__(source = "images/RapidReactField.png", **kwargs)
        self.points = []
        self.selected_point = None

        self.instruction_group_a = InstructionGroup()
        self.instruction_group_b = InstructionGroup()
        

    def draw_path(self):
        self.canvas.remove(self.instruction_group_a)
        self.instruction_group_a = InstructionGroup()
        self.canvas.remove(self.instruction_group_b)
        self.instruction_group_b = InstructionGroup()
        
        for p in self.points:
            pixel_pos = convert.meters_to_pixels((p.x, p.y), self.size)
            if self.selected_point == None:
                self.canvas.add(Color(0.6, 0, 0.6))
                self.instruction_group_a.add(Ellipse(pos = (pixel_pos[0] - 5, pixel_pos[1] - 5), size = (10, 10)))
            elif self.selected_point.index != p.index:
                self.canvas.add(Color(0.6, 0, 0.6))
                self.instruction_group_a.add(Ellipse(pos = (pixel_pos[0] - 5, pixel_pos[1] - 5), size = (10, 10)))
        self.canvas.add(self.instruction_group_a)

        if self.selected_point != None:
            pixel_pos = convert.meters_to_pixels((self.selected_point.x, self.selected_point.y), self.size)
            self.canvas.add(Color(1, 0, 1))
            self.instruction_group_b.add(Ellipse(pos = (pixel_pos[0] - 7, pixel_pos[1] - 7), size = (14, 14)))
        self.canvas.add(self.instruction_group_b)
        

    def get_selected_point(self, px, py):
        for p in self.points:
            pixel_pos = convert.meters_to_pixels((p.x, p.y), self.size)
            if convert.get_dist(px, py, pixel_pos[0], pixel_pos[1]) <= 5:
                self.selected_point = p
                return p
        return None

    def update_points(self, points: list[Point]):
        self.points = points