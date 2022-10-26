from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

from data_assets.point import Point

class PointsMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "vertical", **kwargs)

    #update list of buttons  
    def update_points_list(self, points: list):
        self.clear_widgets()
        for p in points:
            self.add_widget(ToggleButton(text = f"Point {p.index}"))