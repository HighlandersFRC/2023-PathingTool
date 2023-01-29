from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class CommandEditor(Popup):
    def __init__(self, **kwargs):
        super().__init__(title = "Command Editor", **kwargs)

        #list of command objects
        self.commands = []

        #overall layout
        self.layout = BoxLayout(orientation = "vertical")
        self.add_widget(self.layout)

        #sub layouts
        self.commands_layout = GridLayout(cols = 4)
        self.buttons_layout = BoxLayout(orientation = "horizontal")
        self.layout.add_widget(self.commands_layout)
        self.layout.add_widget(self.buttons_layout)

        #buttons for button layout
        self.cancel_button = Button(text = "Cancel", on_press = self.dismiss)
        self.buttons_layout.add_widget(self.cancel_button)

    def update(self, commands: list):
        self.commands = commands

class TimeCommand(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trigger_type = "time"
        self.trigger = 0
        self.command = {
            "type": "",
            "args": []
        }

    def set_type(self, type: str):
        self.command["type"] = type

    def set_args(self, args: list):
        self.command["args"] = args

class PositionCommand(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trigger_type = "position"
        self.trigger = [0, 0]
        self.command = {
            "type": "",
            "args": []
        }
    
    def set_type(self, type: str):
        self.command["type"] = type

    def set_args(self, args: list):
        self.command["args"] = args