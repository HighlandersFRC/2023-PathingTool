from kivy.uix.gridlayout import GridLayout

from widgets.sub_widgets.edit_value import EditValue
from widgets.sub_widgets.nudge_value import NudgeValue
from widgets.sub_widgets.save_delete import SaveDelete
from data_assets.point import Point

class Editor(GridLayout):
    def __init__(self, delete_func, clear_func, **kwargs):
        super().__init__(rows = 4, **kwargs)
        self.selected_point = None

        self.delete_func = delete_func
        self.clear_func = clear_func

        self.edit_x = EditValue("X", "x", self.update_selected_point)
        self.edit_y = EditValue("Y", "y", self.update_selected_point)
        self.nudge_x = NudgeValue("X", "x", self.update_selected_point)
        self.nudge_y = NudgeValue("Y", "y", self.update_selected_point)
        self.save_delete = SaveDelete(self.delete_point, self.clear_points)

        self.add_widget(self.edit_x)
        self.add_widget(self.nudge_x)
        self.add_widget(self.edit_y)
        self.add_widget(self.nudge_y)
        self.add_widget(self.save_delete)

    def delete_point(self):
        if self.selected_point == None:
            return
        self.delete_func(self.selected_point.index)

    def clear_points(self):
        self.clear_func()

    def get_updated_point(self):
        return self.selected_point

    def update_selected_point(self, point):
        self.selected_point = point
        self.edit_x.update(self.selected_point)
        self.edit_y.update(self.selected_point)
        self.nudge_x.update(self.selected_point)
        self.nudge_y.update(self.selected_point)