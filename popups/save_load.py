from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView

class SaveLoad(Popup):
    def __init__(self, **kwargs):
        super().__init__(title = "Save or Load path file", **kwargs)
        self.file_chooser = FileChooserListView()
        self.add_widget(self.file_chooser)