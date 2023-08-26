from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class Switch(BoxLayout):
    def __init__(self, switch_page, **kwargs):
        super().__init__(**kwargs)
        #callback functions
        self.switch_page = switch_page

        #create and add sub-widgets
        self.switch_button = Button(text = "SWITCH PAGE", background_color = (1, 0, 0, 1), on_press = self.switch_func)
        self.add_widget(self.switch_button)

    #delete button callback
    def switch_func(self, event):
        self.switch_page()
