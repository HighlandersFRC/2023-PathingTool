from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from data_assets.point import Point

class VelocityEditor(BoxLayout):
    def __init__(self, update_func, **kwargs):
        super().__init__(**kwargs)
        #selected key point
        self.selected_point = None

        #update callback
        self.update_func = update_func

        #create and add widgets
        self.v_theta_input = TextInput(hint_text = "VTheta (degr)", input_filter = "float")
        self.v_theta_button = Button(text = "Set VTheta", on_press = self.set_v_theta)
        self.v_mag_input = TextInput(hint_text = "VMagnitude (m)", input_filter = "float")
        self.v_mag_button = Button(text = "Set VMagnitude", on_press = self.set_v_mag)
        self.add_widget(self.v_theta_input)
        self.add_widget(self.v_theta_button)
        self.add_widget(self.v_mag_input)
        self.add_widget(self.v_mag_button)

    #set theta component
    def set_v_theta(self, event):
        if self.selected_point == None or self.v_theta_input.text == "":
            return
        self.selected_point.velocity_theta = float(self.v_theta_input.text)
        self.update_func(self.selected_point)

    #set magnitude component
    def set_v_mag(self, event):
        if self.selected_point == None or self.v_mag_input.text == "":
            return
        self.selected_point.velocity_magnitude = float(self.v_mag_input.text)
        self.update_func(self.selected_point)

    #update selected point
    def update(self, point: Point):
        self.selected_point = point
        if self.selected_point == None:
            self.v_theta_input.text = ""
            self.v_mag_input.text = ""
            return
        self.v_theta_input.text = str(round(self.selected_point.velocity_theta, 2))
        self.v_mag_input.text = str(round(self.selected_point.velocity_magnitude, 2))