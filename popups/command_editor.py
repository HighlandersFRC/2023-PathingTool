from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from functools import partial
from data_assets.point import Point

class CommandEditor(Popup):
    def __init__(self, update_func, **kwargs):
        super().__init__(title = "Command Editor", **kwargs)

        #update callback
        self.update_func = update_func

        #list of command objects
        self.commands = []

        #selected key point
        self.selected_point = None

        #overall layout
        self.layout = BoxLayout(orientation = "vertical")
        self.add_widget(self.layout)

        #sub layouts
        self.commands_layout = GridLayout(cols = 4, spacing = 4)
        self.buttons_layout = BoxLayout(orientation = "horizontal", size_hint = (1, 0.1))
        self.layout.add_widget(self.commands_layout)
        self.layout.add_widget(self.buttons_layout)

        #buttons for button layout
        self.cancel_button = Button(text = "Cancel", on_press = self.dismiss)
        self.add_command_button = Button(text = "Add Command", on_press = self.add_command)
        self.buttons_layout.add_widget(self.cancel_button)
        self.buttons_layout.add_widget(self.add_command_button)

    def add_command(self, event):
        self.commands.append(Command(len(self.commands), self.delete_command, self.selected_point))
        self.update_func(self.commands)

    def update(self, commands: list):
        self.commands = commands
        self.index_commands()
        self.commands_layout.clear_widgets()
        for c in self.commands:
            self.commands_layout.add_widget(c)

    def update_selected_point(self, point: Point):
        self.selected_point = point
        for c in self.commands:
            c.selected_point = point

    def index_commands(self):
        for i in range(len(self.commands)):
            self.commands[i].index = i

    def delete_command(self, index: int, event):
        self.commands.pop(index)
        self.update_func(self.commands)

class Command(BoxLayout):
    def __init__(self, index: int, delete_func, selected_point: Point, **kwargs):
        super().__init__(orientation = "horizontal", spacing = 0, **kwargs)
        self.index = index
        self.type = "angle_arm"
        self.args = [180]
        self.trigger_type = "time"
        self.trigger = 0

        self.selected_point = selected_point

        self.type_menu = BoxLayout(orientation = "vertical")
        self.trigger_type_menu = BoxLayout(orientation = "vertical")
        self.trigger_menu = BoxLayout(orientation = "vertical")
        self.extra_menu = BoxLayout(orientation = "vertical")
        self.add_widget(self.type_menu)
        self.add_widget(self.trigger_type_menu)
        self.add_widget(self.trigger_menu)
        self.add_widget(self.extra_menu)

        self.angle_button = Button(text = "Angle\nArm", on_press = partial(self.select_type, "angle"))
        self.extend_button = Button(text = "Extend\nArm", on_press = partial(self.select_type, "extend"))
        self.type_menu.add_widget(self.angle_button)
        self.type_menu.add_widget(self.extend_button)

        self.time_button = Button(text = "Time\nTrigger")
        self.position_button = Button(text = "Position\nTrigger")
        self.trigger_type_menu.add_widget(self.time_button)
        self.trigger_type_menu.add_widget(self.position_button)

        self.time_trigger = BoxLayout(orientation = "horizontal")
        self.position_trigger = BoxLayout(orientation = "horizontal")
        self.index_trigger = BoxLayout(orientation = "horizontal")
        self.trigger_menu.add_widget(self.time_trigger)
        self.trigger_menu.add_widget(self.index_trigger)

        self.time_trigger_input = TextInput(hint_text = "Time", input_filter = "float", multiline = False)
        self.time_trigger_label = Label(text = "[b]Time[/b]", markup = True, outline_color = (1, 0, 0, 1))
        self.time_trigger.add_widget(self.time_trigger_label)
        self.time_trigger.add_widget(self.time_trigger_input)

        self.position_trigger_x_input = TextInput(hint_text = "X", input_filter = "float", multiline = False)
        self.position_trigger_y_input = TextInput(hint_text = "Y", input_filter = "float", multiline = False)
        self.position_trigger_label = Label(text = "[b]Position[/b]", markup = True)
        self.position_trigger.add_widget(self.position_trigger_label)
        self.position_trigger.add_widget(self.position_trigger_x_input)
        self.position_trigger.add_widget(self.position_trigger_y_input)

        self.index_trigger_input = TextInput(hint_text = "Index", input_filter = "int", multiline = False)
        self.index_trigger_label = Label(text = "[b]Point\nIndex[/b]", markup = True)
        self.index_trigger.add_widget(self.index_trigger_label)
        self.index_trigger.add_widget(self.index_trigger_input)

        self.delete_button = Button(text = "Delete", on_press = partial(delete_func, self.index), background_color = (1, 0, 0, 1))
        self.extra_menu.add_widget(self.delete_button)

    def select_type(self, type: str, event):
        self.deselect_all_types()
        if type == "angle":
            self.angle_button.state = "down"
            self.type = "angle_arm"
        elif type == "extend":
            self.extend_button.state = "down"
            self.type = "angle_arm"

    def deselect_all_types(self):
        self.angle_button.state = "normal"
        self.extend_button.state = "normal"

    def get_command(self):
        return {
            "trigger_type": self.trigger_type,
            "trigger": self.trigger,
            "command": {
                "type": self.type,
                "args": self.args
            }
        }