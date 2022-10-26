from kivy.uix.image import Image
from kivy.graphics import *

from data_assets.point import Point
from tools import convert
from SplineGeneration import generateSplines

class Path(Image):
    def __init__(self, **kwargs):
        super().__init__(source = "images/RapidReactField.png", **kwargs)
        #path points and selected point
        self.points = []
        self.selected_point = None

        #robot dimensions
        self.robot_width = 1
        self.robot_length = 1
        self.robot_radius = convert.get_robot_radius(self.robot_)

        #main instructions/instruction groups
        self.non_selected_points_group = InstructionGroup()
        self.selected_points_group = InstructionGroup()
        self.angle_indicators_group = InstructionGroup()
        self.path_line = Line()
        
    #draw points and path line
    def draw_path(self):
        #erase non-selected points, selected point, angle indicators
        self.canvas.remove(self.non_selected_points_group)
        self.non_selected_points_group = InstructionGroup()
        self.canvas.remove(self.selected_points_group)
        self.selected_points_group = InstructionGroup()
        #if path_line instruction is present erase it
        if self.canvas.indexof(self.path_line) != -1:
            self.canvas.remove(self.path_line)

        #if more that 1 point in path generate spline line and add it
        if len(self.points) > 1:
            interp_points = generateSplines.generateSplineCurves([[p.index, p.x, p.y, 0] for p in self.points])
            pixel_list = [None] * (2 * len(interp_points[1]))
            pixel_list[::2] = [convert.meters_to_pixels_x(n, self.size) for n in interp_points[1]]
            pixel_list[1::2] = [convert.meters_to_pixels_y(n, self.size) for n in interp_points[2]]
            self.path_line = Line(points = pixel_list, width = 2, cap = "round", joint = "round")
            self.canvas.add(Color(0, 0, 0))
            self.canvas.add(self.path_line)

        #draw non-selected points and angle indicators
        for p in self.points:
            pixel_pos = convert.meters_to_pixels((p.x, p.y), self.size)

            #non-selected points
            if self.selected_point == None:
                self.canvas.add(Color(0.6, 0, 0.6))
                self.non_selected_points_group.add(Ellipse(pos = (pixel_pos[0] - 5, pixel_pos[1] - 5), size = (10, 10)))
            elif self.selected_point.index != p.index:
                self.canvas.add(Color(0.6, 0, 0.6))
                self.non_selected_points_group.add(Ellipse(pos = (pixel_pos[0] - 5, pixel_pos[1] - 5), size = (10, 10)))

            #angle indicators
            corners = []
        self.canvas.add(self.non_selected_points_group)

        #draw selected point
        if self.selected_point != None:
            pixel_pos = convert.meters_to_pixels((self.selected_point.x, self.selected_point.y), self.size)
            self.canvas.add(Color(1, 0, 1))
            self.selected_points_group.add(Ellipse(pos = (pixel_pos[0] - 7, pixel_pos[1] - 7), size = (14, 14)))
        self.canvas.add(self.selected_points_group)
        
    #return point that was clicked on, if any
    def get_selected_point(self, px, py):
        for p in self.points:
            pixel_pos = convert.meters_to_pixels((p.x, p.y), self.size)
            if convert.get_dist(px, py, pixel_pos[0], pixel_pos[1]) <= 5:
                self.selected_point = p
                return p
        return None

    #update points list
    def update_points(self, points: list):
        self.points = points

    #update selected point
    def update_selected_point(self, point: Point):
        self.selected_point = point