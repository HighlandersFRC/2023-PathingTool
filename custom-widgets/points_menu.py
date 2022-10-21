from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class PointsMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "vertical", **kwargs)
        for i in range(10):
            self.add_widget(Button(text = f"button {i}"))
        