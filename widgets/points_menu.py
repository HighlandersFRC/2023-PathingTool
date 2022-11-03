from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

from data_assets.point import Point
from functools import partial

class PointsMenu(BoxLayout):
    def __init__(self, update_func, **kwargs):
        super().__init__(orientation = "vertical", **kwargs)
        #key points
        self.key_points = []
        #selected key point
        self.selected_point = None
        #update callback
        self.update_func = update_func

        #list of buttons
        self.buttons = []
        #button selected in list
        self.selected_button = None

    #update list of buttons  
    def update(self, key_points: list, selected_point: Point):
        self.clear_widgets()
        self.key_points = key_points
        self.selected_point = selected_point
        self.buttons = []
        for p in self.key_points:
            if selected_point.index == p.index:
                self.buttons.append(ToggleButton(text = f"Point {p.index}", state = "down", on_press = partial(self.select, p.index)))
            else:
                self.buttons.append(ToggleButton(text = f"Point {p.index}", state = "normal", on_press = partial(self.select, p.index)))
        for b in self.buttons:
            self.add_widget(b)

    def select(self, index: int, event):
        self.selected_point = self.key_points[index]
        self.update_func(self.selected_point)
        return index

    #when mouse starts to drag button
    def on_touch_move(self, touch):
        if super().on_touch_move(touch):
            return True

    #when button is selected
    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True