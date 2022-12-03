from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button

from tools import file_manager

class VisualizerMenu(Popup):
    def __init__(self, **kwargs):
        super().__init__(title = "Visualizer Menu", **kwargs)

        self.layout = BoxLayout(orientation = "vertical")
        self.add_widget(self.layout)

        self.data_chooser = FileChooserListView(path = "./recorded_data")
        self.controls_layout = BoxLayout(orientation = "horizontal", size_hint = (1, 0.1))
        self.layout.add_widget(self.data_chooser)
        self.layout.add_widget(self.controls_layout)

        self.graph_button = Button(text = "Graph", on_press = self.graph)
        self.cancel_button = Button(text = "Cancel", on_press = self.cancel)
        self.controls_layout.add_widget(self.graph_button)
        self.controls_layout.add_widget(self.cancel_button)

    def on_open(self):
        file_manager.download_recorded_data("10.44.99.2")
        self.data_chooser._update_files()

    def graph(self, event):
        pass

    def cancel(self, event):
        self.dismiss()