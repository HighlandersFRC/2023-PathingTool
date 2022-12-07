from kivy.uix.image import Image
from kivy.graphics import *

from data_assets.point import Point
from tools import convert
from SplineGeneration import generateSplines
import math
import time

class Path(Image):
    def __init__(self, sample_func, **kwargs):
        super().__init__(source = "images/RapidReactField.png", **kwargs)
        self.key_points = []
        self.sampled_points = []
        self.selected_point = None
        #seconds
        self.sample_rate = 0.01
        #[t, x, y, theta]
        self.recorded_points = []

        #robot dimensions (meters)
        self.robot_width = 0.7366
        self.robot_length = 0.7366
        self.robot_radius = convert.get_robot_radius(self.robot_width, self.robot_length)

        self.field_image = Rectangle(source = "images/RapidReactField.png", pos = self.pos)

        #main instructions/instruction groups
        self.non_selected_points_group = InstructionGroup()
        self.selected_points_group = InstructionGroup()
        self.angle_indicators_group = InstructionGroup()
        self.velocity_indicators_group = InstructionGroup()
        self.animation_group = InstructionGroup()
        self.recording_line = Line()
        self.path_line = Line()

        #animation time (seconds)
        self.animation_time = -1
        self.sample_func = sample_func
        
    #draw points and path line
    def draw_path(self):
        # start_time = time.time_ns() / 1000000
        #erase non-selected points, selected point, angle indicators
        # self.canvas.remove(self.non_selected_points_group)
        self.non_selected_points_group.clear()
        # self.canvas.remove(self.selected_points_group)
        self.selected_points_group.clear()
        # self.canvas.remove(self.angle_indicators_group)
        self.angle_indicators_group.clear()
        # self.canvas.remove(self.velocity_indicators_group)
        self.velocity_indicators_group.clear()
        # self.canvas.remove(self.animation_group)
        self.animation_group.clear()
        #if path_line instruction is present erase it
        # if self.canvas.indexof(self.path_line) != -1:
        #     self.canvas.remove(self.path_line)

        self.canvas.clear()
        self.field_image.size = self.size
        self.canvas.add(self.field_image)
        #if more that 1 point in path generate spline line and add it
        if len(self.key_points) > 1:
            pixel_list = []
            for p in self.sampled_points:
                pixel_list.append(convert.meters_to_pixels_x(p[0], self.size))
                pixel_list.append(convert.meters_to_pixels_y(p[1], self.size))
            self.path_line = Line(points = pixel_list, width = 2, cap = "round", joint = "round")
            self.canvas.add(Color(0, 0, 0))
            self.canvas.add(self.path_line)

        #draw non-selected points and angle indicators
        for p in self.key_points:
            pixel_pos = convert.meters_to_pixels((p.x, p.y), self.size)

            self.non_selected_points_group.add(Color(0.6, 0, 0.6))
            #non-selected points
            if self.selected_point == None:
                self.non_selected_points_group.add(Ellipse(pos = (pixel_pos[0] - 5, pixel_pos[1] - 5), size = (10, 10)))
            elif self.selected_point.index != p.index:
                self.non_selected_points_group.add(Ellipse(pos = (pixel_pos[0] - 5, pixel_pos[1] - 5), size = (10, 10)))

            #angle indicators
            #angle from 0 to first corner
            corner_1_theta = math.atan2((self.robot_length) / (self.robot_radius * 2), (self.robot_width) / (self.robot_radius * 2))
            #corner angles
            theta_1 = corner_1_theta + p.angle
            theta_2 = math.pi - corner_1_theta + p.angle
            theta_3 = math.pi + corner_1_theta + p.angle
            theta_4 = 2 * math.pi - corner_1_theta + p.angle
            #corner coordinates in pixels
            corner_1 = convert.meters_to_pixels((self.robot_radius * math.cos(theta_1) + p.x, self.robot_radius * math.sin(theta_1) + p.y), self.size)
            corner_2 = convert.meters_to_pixels((self.robot_radius * math.cos(theta_2) + p.x, self.robot_radius * math.sin(theta_2) + p.y), self.size)
            corner_3 = convert.meters_to_pixels((self.robot_radius * math.cos(theta_3) + p.x, self.robot_radius * math.sin(theta_3) + p.y), self.size)
            corner_4 = convert.meters_to_pixels((self.robot_radius * math.cos(theta_4) + p.x, self.robot_radius * math.sin(theta_4) + p.y), self.size)
            self.angle_indicators_group.add(Line(width = 2, cap = "square", joint = "miter", close = True, points = [corner_1[0], corner_1[1], corner_2[0], corner_2[1], corner_3[0], corner_3[1], corner_4[0], corner_4[1]]))
            #robot direction indicator
            front = convert.meters_to_pixels(((self.robot_length / 2.0) * math.cos(p.angle) + p.x, (self.robot_length / 2.0) * math.sin(p.angle) + p.y), self.size)
            self.angle_indicators_group.add(Line(width = 2, cap = "square", joint = "miter", points = [pixel_pos[0], pixel_pos[1], front[0], front[1]]))

            #velocity indicators
            self.velocity_indicators_group.add(Color(0, 0.75, 0))
            linear_pos = convert.meters_to_pixels(p.get_vel_marker_pos(), self.size)
            linear_dist = convert.get_dist(pixel_pos[0], pixel_pos[1], linear_pos[0], linear_pos[1])
            self.velocity_indicators_group.add(Line(width = 2, cap = "square", points = [pixel_pos[0], pixel_pos[1], linear_pos[0], linear_pos[1]]))
            # if p.get_angular_velocity_degrees() != 0:
            #     if linear_dist > 20:
            #         self.velocity_indicators_group.add(Line(width = 2, circle = (pixel_pos[0], pixel_pos[1], linear_dist, -p.get_vel_theta_degrees() - p.get_angular_velocity_degrees() + 90, -p.get_vel_theta_degrees() + 90)))
            #     else:
            #         self.velocity_indicators_group.add(Line(width = 2, circle = (pixel_pos[0], pixel_pos[1], 20, -p.get_vel_theta_degrees() - p.get_angular_velocity_degrees() + 90, -p.get_vel_theta_degrees() + 90)))
            
        #animation
        if len(self.key_points) > 1:
            if self.animation_time <= self.key_points[-1].time and self.animation_time >= 0:
                anim_point = self.sample_func(self.animation_time)
                anim_angle = anim_point[2]
                anim_pixel_point = convert.meters_to_pixels((anim_point[0], anim_point[1]), self.size)
                anim_front = convert.meters_to_pixels(((self.robot_length / 2.0) * math.cos(anim_angle) + anim_point[0], (self.robot_length / 2.0) * math.sin(anim_angle) + anim_point[1]), self.size)
                self.animation_group.add(Color(0, 0.4, 0.8))
                self.animation_group.add(Line(width = 2, cap = "square", joint = "miter", points = [anim_pixel_point[0], anim_pixel_point[1], anim_front[0], anim_front[1]]))
                corner_1_theta = math.atan2((self.robot_length) / (self.robot_radius * 2), (self.robot_width) / (self.robot_radius * 2))
                anim_theta_1 = corner_1_theta + anim_angle
                anim_theta_2 = math.pi - corner_1_theta + anim_angle
                anim_theta_3 = math.pi + corner_1_theta + anim_angle
                anim_theta_4 = 2 * math.pi - corner_1_theta + anim_angle
                anim_corner_1 = convert.meters_to_pixels((self.robot_radius * math.cos(anim_theta_1) + anim_point[0], self.robot_radius * math.sin(anim_theta_1) + anim_point[1]), self.size)
                anim_corner_2 = convert.meters_to_pixels((self.robot_radius * math.cos(anim_theta_2) + anim_point[0], self.robot_radius * math.sin(anim_theta_2) + anim_point[1]), self.size)
                anim_corner_3 = convert.meters_to_pixels((self.robot_radius * math.cos(anim_theta_3) + anim_point[0], self.robot_radius * math.sin(anim_theta_3) + anim_point[1]), self.size)
                anim_corner_4 = convert.meters_to_pixels((self.robot_radius * math.cos(anim_theta_4) + anim_point[0], self.robot_radius * math.sin(anim_theta_4) + anim_point[1]), self.size)
                self.animation_group.add(Line(width = 2, cap = "square", joint = "miter", close = True, points = [anim_corner_1[0], anim_corner_1[1], anim_corner_2[0], anim_corner_2[1], anim_corner_3[0], anim_corner_3[1], anim_corner_4[0], anim_corner_4[1]]))
                self.animation_time += 1 / 60
            if self.animation_time > self.key_points[-1].time:
                self.animation_time = 1000
        self.canvas.add(self.velocity_indicators_group)
        self.canvas.add(self.non_selected_points_group)
        self.canvas.add(self.angle_indicators_group)
        self.canvas.add(self.animation_group)

        #draw selected point
        if self.selected_point != None:
            pixel_pos = convert.meters_to_pixels((self.selected_point.x, self.selected_point.y), self.size)
            self.canvas.add(Color(1, 0, 1))
            self.selected_points_group.add(Ellipse(pos = (pixel_pos[0] - 7, pixel_pos[1] - 7), size = (14, 14)))
        self.canvas.add(self.selected_points_group)

        

        # print(f"Draw: {time.time_ns() / 1000000 - start_time}")

    def set_animation(self, time: float):
        self.animation_time = time

    def set_recording(self, recorded_points: list):
        self.recorded_points = recorded_points
        
    #return point that was clicked on, if any
    def get_selected_point(self, px, py):
        for p in self.key_points:
            pixel_pos = convert.meters_to_pixels((p.x, p.y), self.size)
            # vel_marker_pos = convert.meters_to_pixels(p.get_vel_marker_pos(), self.size)
            # if convert.get_dist(px, py, vel_marker_pos[0], vel_marker_pos[1]) <= 5:
            #     return None
            if convert.get_dist(px, py, pixel_pos[0], pixel_pos[1]) <= 7:
                self.selected_point = p
                return p
        return None

    #update points list
    def update(self, points: list[Point], sampled_points: list, sample_rate: float):
        self.key_points = points
        self.sampled_points = sampled_points
        self.sample_rate = sample_rate

    #update selected point
    def update_selected_point(self, point: Point):
        self.selected_point = point