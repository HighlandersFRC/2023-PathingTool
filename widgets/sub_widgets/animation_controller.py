from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class AnimationController(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selecte_point = None

        self.run_full_button = Button(text = "Run Full", on_press = self.run_full)
        self.time_input = TextInput(hint_text = "Time", input_filter = "float")
        self.run_from_time_button = Button(text = "Run from Time", on_press = self.run_from_time)
        self.run_from_point_button = Button(text = "Run from Point", on_press = self.run_from_point)

    def run_full(self):
        pass

    def run_from_time(self):
        pass

    def run_from_point(self):
        pass