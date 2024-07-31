import Calculate
import numpy as np
import json

from manim import *
from manim.utils.color import Colors
from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)

class Animate(Scene):

    def construct(self):

        x = Calculate.x
        y = Calculate.y
        n = Calculate.n
        trails = Calculate.trails
        strings = Calculate.strings

        bobs = []
        lines = []
        colors = []

        with open('colors.json', 'r') as file:
            color_chart = json.load(file)[0]


        background_color_config = Calculate.params.get('background_color')
        background_color = color_chart.get(background_color_config)
        self.camera.background_color = background_color

        #Gets ball color from config
        color_config = Calculate.params.get('ball_colors')
        color_list = color_config.split()
        for color in color_list:
            colors.append(color_chart.get(color))

        #Gets string color from config
        string_color_config = Calculate.params.get('string_color')
        string_color = color_chart.get(string_color_config)

        # Creates updater object for the Strings
        def getline(Point1, Point2):
            start_point = Point1.get_center()
            end_point = Point2.get_center()
            line = Line(start_point, end_point).set_stroke(width=2).set_color(string_color)
            return line

        #Updater to make fading bobs possible
        def fading_updater():
            pass


        # Create the ball and line objects
        for i in range(n):
            if i == 0:
                bobs.append(Dot())
            bobs.append(Dot(radius=0.10).move_to(
                i*RIGHT+i*UP).set_color(colors[i]))
            lines.append(Line(bobs[i], bobs[i+1]).set_stroke(width=2).set_color(string_color))

        # Calls getline for each String
        for i in range(n):
            lines[i].add_updater(lambda mobject, i=i: mobject.become(
                getline(bobs[i], bobs[i+1])))

        # Animation Loop
        for i in range(len(x)):

            Animations = []

            for j in range(len(lines)):
                newloc = [x[i][j],y[i][j], 0] #Initial Position for bobs
                dot = Dot(radius=0.02).move_to(newloc).set_color(colors[j])
                #dot.add_updater(fading_updater(i)), Uncomment this once fading_updater works

                #Conditionals
                if trails and strings:
                    self.add(bobs[j+1], lines[j], dot)
                if trails and not strings:
                    self.add(bobs[j+1], dot)
                if not trails and strings:
                    self.add(lines[j])
                if not trails and not strings:
                    pass

                Animations.append(bobs[j+1].animate.move_to([x[i][j], y[i][j], 0]))

            self.play(*Animations, run_time=1/Calculate.fps)
