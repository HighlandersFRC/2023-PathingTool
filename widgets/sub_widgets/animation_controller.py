from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class AnimationController(BoxLayout):
    def __init__(self, run_func, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        #selected path point
        self.selected_point = None

        #run animation callback
        self.run_func = run_func

        #create and add widgets
        self.run_full_button = Button(text = "Run Full", on_press = self.run_full)
        self.time_input = TextInput(hint_text = "Time", input_filter = "float")
        self.run_from_time_button = Button(text = "Run from Time", on_press = self.run_from_time)
        self.run_from_point_button = Button(text = "Run from Point", on_press = self.run_from_point)
        self.add_widget(self.run_full_button)
        self.add_widget(self.time_input)
        self.add_widget(self.run_from_time_button)
        self.add_widget(self.run_from_point_button)

    #run full animation
    def run_full(self):
        self.run_func(0.0)

    #run animation starting at a time
    def run_from_time(self):
        self.run_func(float(self.time_input.text))

    #run animation starting at the selected point
    def run_from_point(self):
        if self.selected_point == None:
            return
        self.run_func(self.selected_point.time)