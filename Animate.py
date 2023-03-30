import Calculate
import numpy as np

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
        
        bobs = []
        lines = []
        colors = [RED,BLUE,GREEN,YELLOW,ORANGE]

        #Creates updater object for the Strings
        def getline(Point1,Point2):
            start_point = Point1.get_center()
            end_point = Point2.get_center()
            line = Line(start_point,end_point).set_stroke(width=2) 
            return line

        #Create the ball and line objects
        for i in range(n):
            if i == 0:
                bobs.append(Dot())
            bobs.append(Dot(radius=0.05).move_to((i+1.25)*RIGHT+(i+1.25)*UP).set_color(colors[i]))
            lines.append(Line(bobs[i],bobs[i+1]).set_stroke(width = 2))

        #Calls getline for each String
        for i in range(n):
            lines[i].add_updater(lambda mobject, i=i: mobject.become(getline(bobs[i],bobs[i+1])))
        
        #Animation Loop
        for i in range(len(x)):
        
            
            #Trails = []
            Animations = []
            #newloc = bobs[-1].get_center()
            #newloc2 = bobs[-2].get_center()
            #newloc3 = bobs[-3].get_center()
            #dot = Dot(radius=0.02).move_to(newloc).set_color(WHITE)
            #dot2 = Dot(radius=0.02).move_to(newloc2).set_color(BLUE)
            #dot3 = Dot(radius=0.02).move_to(newloc3).set_color(RED)
            #self.add(dot,dot2,dot3)
            
            for j in range(len(lines)):
            	newloc = bobs[j+1].get_center()
            	dot = Dot(radius=0.02).move_to(newloc).set_color(colors[j])
            	self.remove(bobs[j+1])
            	self.add(bobs[j+1],lines[j],dot)
            	Animations.append(bobs[j+1].animate.move_to([x[i][j],y[i][j],0]))

            self.play(*Animations, run_time = 1/Calculate.fps)
            
