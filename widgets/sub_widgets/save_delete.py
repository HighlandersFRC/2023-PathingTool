from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class SaveDelete(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_button = Button(text = "CLEAR", background_color = (1, 0, 0, 1), on_press = self.clear)
        self.delete_button = Button(text = "DELETE", background_color = (1, 0, 0, 1), on_press = self.delete)
        self.save_button = Button(text = "SAVE", background_color = (0, 1, 0, 1), on_press = self.save)
        self.add_widget(self.clear_button)
        self.add_widget(self.delete_button)
        self.add_widget(self.save_button)

    def save(self, event):
        pass

    def delete(self, event):
        pass

    def clear(self, event):
        pass