from kivy.uix.boxlayout import BoxLayout

from widgets.path import Path
from widgets.points_menu import PointsMenu
from widgets.editor import Editor
from data_assets.point import Point
from tools import convert

class PathTool(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        self.editor_viewer_layout = BoxLayout(orientation = "vertical")
        self.editor = Editor(size_hint = (1, 0.25))
        self.path = Path(size_hint = (1, 0.75), allow_stretch = True, keep_ratio = False)
        self.points_menu = PointsMenu(size_hint = (0.1, 1), padding = [2, 2, 2, 2], spacing = 1)
        self.set_layout()

        self.points = []
        self.selected_point = None

    def set_layout(self):
        self.editor_viewer_layout.add_widget(self.editor)
        self.editor_viewer_layout.add_widget(self.path)
        self.add_widget(self.editor_viewer_layout)
        self.add_widget(self.points_menu)

    def on_touch_up(self, touch):
        if super().on_touch_up(touch):
            return True

        #Click on the field
        if self.path.collide_point(touch.x, touch.y):
            self.selected_point = self.path.get_selected_point(touch.x, touch.y)
            if self.selected_point == None:
                pos = convert.pixels_to_meters((touch.x, touch.y), self.path.size)
                self.selected_point = Point(len(self.points), pos[0], pos[1])
                self.points.append(self.selected_point)
            else:
                self.editor.update_selected_point(self.selected_point)

        #Click on the editor
        if self.editor.collide_point(touch.x, touch.y):
            self.selected_point = self.editor.get_updated_point()
            if self.selected_point == None:
                return True
            else:
                self.points[self.selected_point.index] = self.selected_point

        #Update main widgets
        self.path.update_points(self.points)
        self.points_menu.update_points_list(self.points)
