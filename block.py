from turtle import Turtle


class BorderBlock:

    WIDTH = 30
    HEIGHT = 30

    def __init__(self, start_pos: tuple[int, int]):
        self.turtle = Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.turtle.pencolor("black")
        self.turtle.penup()
        self.turtle.goto(start_pos)
        self.turtle.pendown()
        self.turtle.begin_fill()
        for i in range(2):
            self.turtle.forward(self.WIDTH)
            self.turtle.right(90)
            self.turtle.forward(self.HEIGHT)
            self.turtle.right(90)
        self.turtle.end_fill()
