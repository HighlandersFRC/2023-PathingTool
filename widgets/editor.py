from kivy.uix.gridlayout import GridLayout

from widgets.sub_widgets.edit_value import EditValue
from data_assets.point import Point

class Editor(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(rows = 3, **kwargs)
        self.selected_point = None

        self.edit_x = EditValue("X", "x", self.update_selected_point)
        self.edit_y = EditValue("Y", "y", self.update_selected_point)

        self.add_widget(self.edit_x)
        self.add_widget(self.edit_y)

    def get_updated_point(self):
        return self.selected_point

    def update_selected_point(self, point):
        self.selected_point = point
        self.edit_x.update(self.selected_point)
        self.edit_y.update(self.selected_point)