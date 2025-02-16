# conda activate my-manim-environment
# cd my-project
# subl .
# manim -pql main.py DefaultTemplate

from manim import *
#############################################

# square to circle transformation
# class DefaultTemplate(Scene):
#     def construct(self):
#         circle = Circle()  # create a circle
#         circle.set_fill(PINK, opacity=0.5)  # set color and transparency

#         square = Square()  # create a square
#         square.flip(RIGHT)  # flip horizontally
#         square.rotate(-3 * TAU / 8)  # rotate a certain amount

#         self.play(Create(square))  # animate the creation of the square
#         self.play(Transform(square, circle))  # interpolate the square into the circle
#         self.play(FadeOut(square))  # fade out animation

##############################################

# square to circle + color change 
class DefaultTemplate(Scene):
    def construct(self):
        circle = Circle()  
        circle.set_fill(PINK, opacity=0.5)  # set initial color and transparency

        square = Square()  
        square.flip(RIGHT)  
        square.rotate(-3 * TAU / 8)  

        self.play(Create(square))

        # new: make square change to blue color 
        self.play(square.animate.set_color(BLUE))

        self.play(Transform(square, circle))

        # new: change color of circle to green with set_color
        self.play(circle.animate.set_color(GREEN)) 
        self.play(FadeOut(square))

############################################

# class SquareToCircle(Scene):
#     def construct(self):
#         circle = Circle()  # create a circle
#         circle.set_fill(PINK, opacity=0.5)  # set color and transparency

#         square = Square()  # create a square
#         square.rotate(PI / 4)  # rotate a certain amount

#         self.play(Create(square))  # animate the creation of the square
#         self.play(Transform(square, circle))  # interpolate the square into the circle
#         self.play(FadeOut(square))  # fade out animation

# manim -pql main.py SquareToCircle

#############################################

# class CreateCircle(Scene):
#     def construct(self):
#         circle = Circle()  # create a circle
#         circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
#         self.play(Create(circle))  # show the circle on screen

# manim -pql main.py CreateCircle
