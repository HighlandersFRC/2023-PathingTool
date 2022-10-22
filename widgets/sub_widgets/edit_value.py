from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from data_assets.point import Point

class EditValue(BoxLayout):
    def __init__(self, name: str, field: str, update_func, **kwargs):
        super().__init__(**kwargs)
        self.selected_point = None

        self.update_func = update_func
        self.name = name
        self.field = field
        self.value_input = TextInput(hint_text = f"{self.name} value", input_filter = "float")
        self.submit_button = Button(text = f"Set {self.name}", on_press = self.submit)
        self.add_widget(self.value_input)
        self.add_widget(self.submit_button)

    def submit(self, event):
        if self.selected_point == None:
            return
        value = float(self.value_input.text)
        if value == "":
            return
        self.set_value(value)
        self.update_func(self.selected_point)

    def update(self, point):
        self.selected_point = point
        self.value_input.text = str(round(self.get_value(), 2))

    def get_value(self):
        if self.selected_point == None:
            return ""
        if self.field == "x":
            return self.selected_point.x
        if self.field == "y":
            return self.selected_point.y

    def set_value(self, value):
        if self.selected_point == None:
            return
        if self.field == "x":
            self.selected_point.x = value
        if self.field == "y":
            self.selected_point.y = value
           