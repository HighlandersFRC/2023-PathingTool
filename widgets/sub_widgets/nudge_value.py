from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class NudgeValue(BoxLayout):
    def __init__(self, name: str, field: str, update_func, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        self.selected_point = None

        self.name = name
        self.field = field
        self.update_func = update_func
        self.increment_button = Button(text = f"+{self.name}", on_press = self.increment)
        self.decrement_button = Button(text = f"-{self.name}", on_press = self.decrement)
        self.add_widget(self.decrement_button)
        self.add_widget(self.increment_button)

    def increment(self, event):
        if self.selected_point == None:
            return
        self.set_value(self.get_value() + 0.025)
        self.update_func(self.selected_point)

    def decrement(self, event):
        if self.selected_point == None:
            return
        self.set_value(self.get_value() - 0.025)
        self.update_func(self.selected_point)

    def update(self, point):
        self.selected_point = point

    def get_value(self):
        if self.selected_point == None:
            return 0
        if self.field == "x":
            return self.selected_point.x
        if self.field == "y":
            return self.selected_point.y

    def set_value(self, value: float):
        if self.selected_point == None:
            return
        if self.field == "x":
            self.selected_point.x = value
        if self.field == "y":
            self.selected_point.y = value