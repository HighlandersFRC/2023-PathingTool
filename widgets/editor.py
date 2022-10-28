from kivy.uix.gridlayout import GridLayout

from widgets.sub_widgets.angle_selector import AngleSelector
from widgets.sub_widgets.edit_value import EditValue
from widgets.sub_widgets.nudge_value import NudgeValue
from widgets.sub_widgets.save_delete import SaveDelete
from widgets.sub_widgets.animation_controller import AnimationController
from data_assets.point import Point

class Editor(GridLayout):
    def __init__(self, delete_func, clear_func, **kwargs):
        super().__init__(rows = 4, **kwargs)
        #selected path point
        self.selected_point = None

        #callback functions in pathtool
        self.delete_func = delete_func
        self.clear_func = clear_func

        #editor sub-widgets
        self.edit_time = EditValue("Delta Time", "delta_time", self.update_selected_point)
        self.edit_x = EditValue("X", "x", self.update_selected_point)
        self.edit_y = EditValue("Y", "y", self.update_selected_point)
        self.angle_selector = AngleSelector(self.update_selected_point)
        self.nudge_x = NudgeValue("X", "x", self.update_selected_point)
        self.nudge_y = NudgeValue("Y", "y", self.update_selected_point)
        self.save_delete = SaveDelete(self.delete_point, self.clear_points)
        self.animation_controller = AnimationController(self.run_animation)

        #add sub-widgets
        self.add_widget(self.edit_time)
        self.add_widget(self.edit_x)
        self.add_widget(self.nudge_x)
        self.add_widget(self.edit_y)
        self.add_widget(self.nudge_y)
        self.add_widget(self.angle_selector)
        self.add_widget(self.save_delete)
        self.add_widget(self.animation_controller)

    #delete selected point if a point is selected
    def delete_point(self):
        if self.selected_point == None:
            return
        #call callback in pathtool
        self.delete_func(self.selected_point.index)

    #clear points by calling callback in pathtool
    def clear_points(self):
        self.clear_func()

    #return the updated selected point
    def get_updated_point(self):
        return self.selected_point

    #update selected point and update sub-widgets
    def update_selected_point(self, point: Point):
        self.selected_point = point
        self.edit_time.update(self.selected_point)
        self.edit_x.update(self.selected_point)
        self.edit_y.update(self.selected_point)
        self.angle_selector.update(self.selected_point)
        self.nudge_x.update(self.selected_point)
        self.nudge_y.update(self.selected_point)

    def run_animation(self, time: float):
        pass
