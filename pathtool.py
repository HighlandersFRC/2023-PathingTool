from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from widgets.path import Path
from widgets.points_menu import PointsMenu
from widgets.editor import Editor
from data_assets.point import Point
from tools import convert
from tools import file_manager
from popups.save_load import SaveLoad
import math

class PathTool(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        #main widgets
        self.editor_viewer_layout = BoxLayout(orientation = "vertical")
        self.editor = Editor(self.delete_point, self.clear_points, self.run_animation, self.save_path, self.load_path, self.upload_path, self.upload_all_paths, self.download_all_paths, self.average_linear_velocities, self.average_angular_velocities, size_hint = (1, 0.25))
        self.path = Path(size_hint = (1, 1.5), allow_stretch = True, keep_ratio = False)
        self.points_menu = PointsMenu(self.update_path, size_hint = (0.1, 1), padding = [2, 2, 2, 2], spacing = 1)
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
                if len(self.key_points) > 0:
                    self.selected_point = Point(len(self.key_points), 1.0, pos[0], pos[1], 0.0, 1.0, 0.0, 0.0)
                else:
                    self.selected_point = Point(len(self.key_points), 0.0, pos[0], pos[1], 0.0, 0.0, 0.0, 0.0)
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
        self.points_menu.update(self.key_points, self.selected_point)
        #update selected point in widgets
        self.editor.update_selected_point(self.selected_point)
        self.editor.update_path_name(self.path_name)
        self.path.update_selected_point(self.selected_point)

    #update key points and selected point
    def update_path(self, key_points: list[Point], selected_point: Point):
        self.selected_point = selected_point
        self.key_points = key_points
        self.update_widgets()

    #delete selected point
    def delete_point(self, index):
        #if removed point is the first point set new first point velocity to zero
        if index == 0 and len(self.key_points) > 1:
            self.key_points[1].velocity_magnitude = 0
            self.key_points[1].delta_time = 0
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

    #set average velocities for sandwiched points and zero velocities for edge points
    def average_linear_velocities(self):
        for p in self.key_points:
            if p.index != 0 and p.index != len(self.key_points) - 1:
                p0 = self.key_points[p.index - 1]
                p2 = self.key_points[p.index + 1]
                dt = p2.time - p0.time
                v_theta = math.atan2(p2.y - p0.y, p2.x - p0.x)
                dist = convert.get_dist(p0.x, p0.y, p2.x, p2.y)
                v_mag = dist / dt
                p.velocity_magnitude = v_mag
                p.velocity_theta = v_theta
            else:
                p.velocity_magnitude = 0
                p.velocity_theta = 0
        self.update_widgets()

    def average_angular_velocities(self):
        for p in self.key_points:
            if p.index != 0 and p.index != len(self.key_points) - 1:
                p0 = self.key_points[p.index - 1]
                p2 = self.key_points[p.index + 1]
                dt = p2.time - p0.time
                da = p2.angle - p0.angle
                if p2.angle - p0.angle > math.pi:
                    da = math.pi - da
                elif p2.angle - p0.angle < -math.pi:
                    da = math.pi + da
                sine1 = self.get_optimized_rotation_sine(p0.angle, p.angle)
                sine2 = self.get_optimized_rotation_sine(p.angle, p2.angle)
                if sine1 != sine2:
                    p.angular_velocity = 0
                else:
                    p.angular_velocity = da / dt
            else:
                p.angular_velocity = 0
        self.update_widgets()

    def get_optimized_rotation_sine(self, angle1, angle2):
        if angle1 >= angle2:
            op2 = ((math.pi * 2) - (angle1 - angle2))
            op1 = (angle1 - angle2)
        else:
            op1 = ((math.pi * 2) - (angle2 - angle1))
            op2 = (angle2 - angle1)
        if op1 <= op2:
            return -1
        else:
            return 1

    #start path animation from a time
    def run_animation(self, start_time: float):
        self.path.set_animation(start_time)

    #save path as json file
    def save_path(self, folder_path: str, file_name: str, sample_rate: float):
        print(f"saving {folder_path}\\{file_name}.json")
        self.sample_rate = sample_rate
        self.path_name = file_name
        result = file_manager.save_path(self.key_points, self.sample_rate, folder_path, file_name)
        self.update_widgets()
        #update status
        if result:
            self.editor.update_status("[b]Path Saved[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Save Failed[/b]", (1, 0.25, 0.25, 1))

    #open json save file
    def load_path(self, file_path: str):
        print(f"loading {file_path}")
        path_data = file_manager.load_path(file_path)
        self.key_points = path_data[0]
        self.sample_rate = path_data[1]
        self.path_name = path_data[2]
        self.selected_point = None
        self.update_widgets()
        #update status
        if self.path_name == "":
            self.editor.update_status("[b]Load Failed[/b]", (1, 0.25, 0.25, 1))
        else:
            self.editor.update_status("[b]Path Loaded[/b]", (0.25, 1, 0.25, 1))

    #upload the current path
    def upload_path(self, file_path: str, folder_path: str, file_name: str, sample_rate: float):
        self.save_path(folder_path, file_name, sample_rate)
        result = file_manager.upload("10.44.99.2", file_path)
        #update status
        if result:
            self.editor.update_status("[b]Path Uploaded[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Upload Failed[/b]", (1, 0.25, 0.25, 1))

    #upload all paths
    def upload_all_paths(self, folder_path: str, file_name: str, sample_rate: float):
        self.save_path(folder_path, file_name, sample_rate)
        result = file_manager.upload_all("10.44.99.2")
        #update status
        if result:
            self.editor.update_status("[b]Uploaded All Paths[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Upload All Failed[/b]", (1, 0.25, 0.25, 1))

    #download all paths
    def download_all_paths(self):
        result = file_manager.download_all("10.44.99.2")
        #update status
        if result:
            self.editor.update_status("[b]All Paths Downloaded[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Download All Failed[/b]", (1, 0.25, 0.25, 1))