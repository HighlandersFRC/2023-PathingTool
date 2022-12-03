from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class ExtraControls(BoxLayout):
    def __init__(self, cat_func, **kwargs):
        super().__init__(**kwargs)
        #catmull-rom callback
        self.cat_func = cat_func
        
        #create and add widgets
        self.catmull_rom_button = Button(text = "Cat. ALL", on_press = self.cat_all, background_color = (0.5, 0, 0, 1))
        self.add_widget(self.catmull_rom_button)

    #catmull-rom all button callback
    def cat_all(self, event):
        self.cat_func()