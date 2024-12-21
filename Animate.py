import Calculate
import numpy as np
import json
from manim import *
from manim.utils.color import Colors
from configparser import ConfigParser
from collections import deque

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

        # Load colors once at initialization
        with open('colors.json', 'r') as file:
            color_chart = json.load(file)[0]

        # Set background color
        background_color_config = Calculate.params.get('background_color')
        self.camera.background_color = color_chart.get(background_color_config)

        # Process colors once
        color_list = Calculate.params.get('ball_colors').split()
        colors = [color_chart.get(color) for color in color_list]
        string_color = color_chart.get(Calculate.params.get('string_color'))

        # Initialize bobs and lines
        bobs = [Dot()]  # Initial anchor point
        lines = []

        # Create VGroups for trails (one per bob)
        MAX_TRAIL_LENGTH = 50  # Adjust this value to control trail length
        trail_groups = [VGroup() for _ in range(n)]
        trail_points = [deque(maxlen=MAX_TRAIL_LENGTH) for _ in range(n)]

        # Create bobs and lines
        for i in range(n):
            bob = Dot(radius=0.10).move_to([x[0][i], y[0][i], 0]).set_color(colors[i])
            bobs.append(bob)

            if strings:
                line = Line(bobs[i], bob).set_stroke(width=2).set_color(string_color)
                lines.append(line)

        # Add objects to scene
        for i in range(n):
            if strings:
                self.add(lines[i])
            self.add(bobs[i + 1])
            if trails:
                self.add(trail_groups[i])

        # Define line updater function
        def update_line(line, i):
            line.put_start_and_end_on(
                bobs[i].get_center(),
                bobs[i + 1].get_center()
            )

        # Add updaters to lines
        if strings:
            for i in range(n):
                lines[i].add_updater(lambda m, i=i: update_line(m, i))

        # Animate using physics timesteps
        dt = 1/Calculate.fps
        for frame in range(len(x)):
            animations = []

            # Update trails
            if trails:
                for j in range(n):
                    pos = [x[frame][j], y[frame][j], 0]
                    trail_points[j].append(pos)

                    # Remove old trail group and create new one
                    self.remove(trail_groups[j])
                    trail_groups[j] = VGroup()

                    # Create dots with variable opacity
                    points_list = list(trail_points[j])
                    for idx, point in enumerate(points_list):
                        opacity = (idx + 1) / len(points_list)  # Newer points are more opaque
                        dot = Dot(
                            point=point,
                            radius=0.02,
                            color=colors[j],
                            fill_opacity = opacity
                        )
                        trail_groups[j].add(dot)

                    self.add(trail_groups[j])

            # Animate bob movements
            for j in range(n):
                pos = [x[frame][j], y[frame][j], 0]
                animations.append(bobs[j + 1].animate.move_to(pos))

            self.play(
                *animations,
                run_time=dt,
                rate_func=linear
            )

        # Clean up
        if strings:
            for line in lines:
                line.clear_updaters()
