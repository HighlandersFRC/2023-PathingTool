from kivy.uix.boxlayout import BoxLayout

from custom_widgets.path import Path
from custom_widgets.points_menu import PointsMenu
from custom_widgets.editor import Editor
from data_assets.point import Point
from tools import convert

class PathTool(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        self.editor_viewer_layout = BoxLayout(orientation = "vertical")
        self.editor = Editor(size_hint = (1, 0.25))
        self.path = Path(size_hint = (1, 0.75))
        self.points_menu = PointsMenu(size_hint = (0.1, 1))
        self.set_layout()

        self.points = []
        self.selected_point = None

    def set_layout(self):
        self.editor_viewer_layout.add_widget(self.editor)
        self.editor_viewer_layout.add_widget(self.path)
        self.add_widget(self.editor_viewer_layout)
        self.add_widget(self.points_menu)

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if self.path.collide_point(touch.x, touch.y):
            self.selected_point = self.path.get_selected_point(touch.x, touch.y)
            if self.selected_point == None:
                pos = convert.pixel_to_meters((touch.x, touch.y))
                self.selected_point = Point(len(self.points), pos[0], pos[1], touch.x, touch.y)
                self.points.append(self.selected_point)
                self.path.update_points(self.points)
                self.points_menu.update_points_list(self.points)
