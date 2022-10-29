from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from widgets.path import Path
from widgets.points_menu import PointsMenu
from widgets.editor import Editor
from data_assets.point import Point
from tools import convert
from popups.save_load import SaveLoad

class PathTool(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        #main widgets
        self.editor_viewer_layout = BoxLayout(orientation = "vertical")
        self.editor = Editor(self.delete_point, self.clear_points, self.run_animation, size_hint = (1, 0.25))
        self.path = Path(size_hint = (1, 1.5), allow_stretch = True, keep_ratio = False)
        self.points_menu = PointsMenu(size_hint = (0.1, 1), padding = [2, 2, 2, 2], spacing = 1)
        self.set_layout()

        #list of key points
        self.points = []
        #currently selected point
        self.selected_point = None

        #save and load path popup
        self.save_load_popup = SaveLoad()
        self.save_load_popup.open()

    #add widgets to main layout
    def set_layout(self):
        self.editor_viewer_layout.add_widget(self.editor)
        self.editor_viewer_layout.add_widget(self.path)
        self.add_widget(self.editor_viewer_layout)
        self.add_widget(self.points_menu)

    #called on click events
    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True

        #Click on the field
        if self.path.collide_point(touch.x, touch.y):
            self.selected_point = self.path.get_selected_point(touch.x, touch.y)

            #if no point is selected add new point
            if self.selected_point == None:
                pos = convert.pixels_to_meters((touch.x, touch.y), self.path.size)
                self.selected_point = Point(len(self.points), 1.0, pos[0], pos[1], 0.0)
                self.points.append(self.selected_point)
            #else update selected point
            else:
                self.editor.update_selected_point(self.selected_point)

        #Click on the editor
        if self.editor.collide_point(touch.x, touch.y):
            self.selected_point = self.editor.get_updated_point()

            #if no point is selected do nothing
            if self.selected_point == None:
                return True
            #else update selected point
            else:
                self.points[self.selected_point.index] = self.selected_point

        #update main widgets
        self.update_widgets()

    #update main widgets
    def update_widgets(self):
        #update indexes and times
        self.index_points()
        self.time_points()
        #update key points in widgets
        self.path.update_points(self.points)
        self.points_menu.update_points_list(self.points)
        #update selected point in widgets
        self.editor.update_selected_point(self.selected_point)
        self.path.update_selected_point(self.selected_point)

    #delete selected point
    def delete_point(self, index):
        #remove point
        self.points.pop(index)
        #if removed point is the selected point (which it should be) clear selected point
        if self.selected_point.index == index:
            self.selected_point = None
        #update main widgets
        self.update_widgets()

    #clear key points
    def clear_points(self):
        #clear key points, selected point, and update main widgets
        self.points = []
        self.selected_point = None
        self.update_widgets()

    #re-index points
    def index_points(self):
        for i in range(len(self.points)):
            self.points[i].index = i

    #update time values for each point
    def time_points(self):
        time = 0.0
        for p in self.points:
            time += p.delta_time
            p.time = time

    #start path animation from a time
    def run_animation(self, start_time: float):
        self.path.set_animation(start_time)