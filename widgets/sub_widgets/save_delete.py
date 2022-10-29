from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class SaveDelete(BoxLayout):
    def __init__(self, delete_point, clear_points, save_func, open_func, upload_func, **kwargs):
        super().__init__(**kwargs)
        #callback functions
        self.delete_point = delete_point
        self.clear_points = clear_points
        self.save_func = save_func
        self.open_func = open_func
        self.upload_func = upload_func

        #create and add sub-widgets
        self.clear_button = Button(text = "CLEAR", background_color = (0.5, 0, 0, 1), on_press = self.clear)
        self.delete_button = Button(text = "DELETE", background_color = (1, 0, 0, 1), on_press = self.delete)
        self.save_button = Button(text = "SAVE", background_color = (0, 0.5, 0, 1), on_press = self.save)
        self.open_button = Button(text = "OPEN", background_color = (0, 1, 0, 1), on_press = self.open)
        self.upload_button = Button(text = "UPLOAD", background_color = (0, 0.5, 0, 1), on_press = self.upload)
        self.add_widget(self.clear_button)
        self.add_widget(self.delete_button)
        self.add_widget(self.save_button)
        self.add_widget(self.open_button)
        self.add_widget(self.upload_button)

    #updload button callback
    def upload(self, event):
        self.upload_func()

    #save button callback
    def save(self, event):
        self.save_func()

    #open button callback
    def open(self, event):
        self.open_func

    #delete button callback
    def delete(self, event):
        self.delete_point()

    #clear button callback
    def clear(self, event):
        self.clear_points()