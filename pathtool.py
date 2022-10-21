from kivy.uix.boxlayout import BoxLayout

from custom_widgets.path import Path
from custom_widgets.points_menu import PointsMenu

class PathTool:
    def __init__(self):
        self.layout = BoxLayout(orientation = "horizontal")
        self.path = Path(size_hint = (0.9, 1))
        self.points_menu = PointsMenu(size_hint = (0.1, 1))
        self.setLayout()

    def setLayout(self):
        self.layout.add_widget(self.path)
        self.layout.add_widget(self.points_menu)
