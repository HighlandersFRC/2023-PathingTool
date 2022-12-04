from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class ExtraControls(BoxLayout):
    def __init__(self, cat_func, visualize_func, **kwargs):
        super().__init__(**kwargs)
        #callbacks
        self.cat_func = cat_func
        self.visualize_func = visualize_func
        
        #create and add widgets
        self.catmull_rom_button = Button(text = "Cat. ALL", on_press = self.cat_all, background_color = (0.5, 0, 0, 1))
        self.visualize_button = Button(text = "Visualizer", on_press = self.visualize)
        self.add_widget(self.catmull_rom_button)
        self.add_widget(self.visualize_button)

    #catmull-rom all button callback
    def cat_all(self, event):
        self.cat_func()

    def visualize(self, event):
        self.visualize_func()