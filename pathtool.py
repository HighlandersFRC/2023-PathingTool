from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from widgets.path import Path
from widgets.points_menu import PointsMenu
from widgets.editor import Editor
from data_assets.point import Point
from tools import convert
from tools import file_manager
from popups.save_load import SaveLoad

class PathTool(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        #main widgets
        self.editor_viewer_layout = BoxLayout(orientation = "vertical")
        self.editor = Editor(self.delete_point, self.clear_points, self.run_animation, self.save_path, self.load_path, size_hint = (1, 0.25))
        self.path = Path(size_hint = (1, 1.5), allow_stretch = True, keep_ratio = False)
        self.points_menu = PointsMenu(size_hint = (0.1, 1), padding = [2, 2, 2, 2], spacing = 1)
        self.set_layout()

        #list of key points
        self.key_points = []
        #currently selected point
        self.selected_point = None
        #how often path is sample in seconds
        self.sample_rate = 0.01
        #name of current path
        self.path_name = ""

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
                self.selected_point = Point(len(self.key_points), 1.0, pos[0], pos[1], 0.0)
                self.key_points.append(self.selected_point)
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
                self.key_points[self.selected_point.index] = self.selected_point

        #update main widgets
        self.update_widgets()

    #update main widgets
    def update_widgets(self):
        #update indexes and times
        self.index_points()
        self.time_points()
        #update key points in widgets
        self.path.update(self.key_points, self.sample_rate)
        self.points_menu.update_points_list(self.key_points)
        #update selected point in widgets
        self.editor.update_selected_point(self.selected_point)
        self.editor.update_path_name(self.path_name)
        self.path.update_selected_point(self.selected_point)

    #delete selected point
    def delete_point(self, index):
        #remove point
        self.key_points.pop(index)
        #if removed point is the selected point (which it should be) clear selected point
        if self.selected_point.index == index:
            self.selected_point = None
        #update main widgets
        self.update_widgets()

    #clear key points
    def clear_points(self):
        #clear key points, selected point, and update main widgets
        self.key_points = []
        self.selected_point = None
        self.update_widgets()

    #re-index points
    def index_points(self):
        for i in range(len(self.key_points)):
            self.key_points[i].index = i

    #update time values for each point
    def time_points(self):
        time = 0.0
        for p in self.key_points:
            time += p.delta_time
            p.time = time

    #start path animation from a time
    def run_animation(self, start_time: float):
        self.path.set_animation(start_time)

    #save path as json file
    def save_path(self, folder_path: str, file_name: str):
        print(f"saving {folder_path}\\{file_name}.json")
        file_manager.save_path(self.key_points, self.sample_rate, folder_path, file_name)

    #open json save file
    def load_path(self, file_path: str):
        print(f"loading {file_path}")
        path_data = file_manager.load_path(file_path)
        self.key_points = path_data[0]
        self.sample_rate = path_data[1]
        self.path_name = path_data[2]
        self.selected_point = None
        self.update_widgets()
        