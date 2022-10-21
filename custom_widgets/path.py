from kivy.uix.image import Image

from data_assets.point import Point
from tools import convert

class Path(Image):
    def __init__(self, **kwargs):
        super().__init__(source = "images/RapidReactField.png", **kwargs)
        self.points = []

    def draw_path(self):
        self.canvas.clear()

    def get_selected_point(self, x, y):
        for p in self.points:
            if convert.get_dist(x, y, p.x, p.y) <= 3:
                return p
        return None

    def update_points(self, points: list[Point]):
        self.points = points