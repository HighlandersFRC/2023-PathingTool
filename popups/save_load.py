from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class SaveLoad(Popup):
    def __init__(self, save_func, load_func, **kwargs):
        super().__init__(title = "Save or Load path file", **kwargs)

        #callback functions
        self.save_func = save_func
        self.load_func = load_func

        #main layout
        self.layout = BoxLayout(orientation = "vertical")
        self.add_widget(self.layout)

        #sub-layout for text box and buttons
        self.controls_layout = BoxLayout(orientation = "horizontal", size_hint = (1, 0.08))

        #Create and add widgets
        self.file_chooser = FileChooserListView(path = "./saves")
        self.text_box = TextInput(hint_text = "File name")
        self.load_button = Button(text = "Load", on_press = self.load, size_hint = (0.2, 1))
        self.save_button = Button(text = "Save", on_press = self.save, size_hint = (0.2, 1))
        self.path_label = Label(text = "", size_hint = (1, 0.05))
        self.layout.add_widget(self.path_label)
        self.layout.add_widget(self.file_chooser)
        self.layout.add_widget(self.controls_layout)
        self.controls_layout.add_widget(self.text_box)
        self.controls_layout.add_widget(self.load_button)
        self.controls_layout.add_widget(self.save_button)

    #save path
    def save(self, event):
        if not "saves" in self.file_chooser.path or self.text_box.text == "":
            return
        self.save_func(self.file_chooser.path, self.text_box.text)
        self.dismiss()

    #load path
    def load(self, event):
        if not "saves" in self.file_chooser.path or self.file_chooser.selection == []:
            return
        self.load_func(self.file_chooser.selection[0])
        self.dismiss()

    #update callback
    def update(self):
        self.path_label.text = self.file_chooser.path
        if len(self.file_chooser.selection) > 0:
            self.text_box.text = self.file_chooser.selection[0]