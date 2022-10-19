from kivy.uix.boxlayout import BoxLayout

from custom_widgets.path import Path
from custom_widgets.points_menu import PointsMenu

class PathTool:
    def __init__(self):
        self.layout = BoxLayout()
        self.path = Path()
        self.points_menu = PointsMenu()
        