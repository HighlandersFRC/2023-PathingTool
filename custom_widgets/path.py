from kivy.uix.image import Image
from kivy.graphics import *

from data_assets.point import Point
from tools import convert

class Path(Image):
    def __init__(self, **kwargs):
        super().__init__(source = "images/RapidReactField.png", **kwargs)
        self.points = []
        self.instruction_group = InstructionGroup()

    def draw_path(self):
        self.instruction_group = InstructionGroup()
        self.canvas.remove_group("instruction_group")
        for p in self.points:
            self.canvas.add(Color(1, 0, 0))
            self.instruction_group.add(Ellipse(pos = (p.px, p.py), size = (6, 6)))
        self.canvas.add(self.instruction_group)
        

    def get_selected_point(self, px, py):
        for p in self.points:
            if convert.get_dist(px, py, p.px, p.py) <= 3:
                return p
        return None

    def update_points(self, points: list[Point]):
        self.points = points