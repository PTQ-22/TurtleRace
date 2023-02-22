from turtle import Turtle

from block import Block


class Player:

    SPEED = 10

    def __init__(self, start_pos: tuple[int, int], color: str):
        self.turtle = Turtle()
        # self.turtle.turtlesize(1.5)
        self.turtle.penup()
        self.turtle.setposition(start_pos)
        self.turtle.shape("turtle")
        self.turtle.color(color)
        self.last_move = 'right'

    def is_collided_with(self, other: Block) -> bool:
        t1_width = self.turtle.shapesize()[0]
        t1_height = self.turtle.shapesize()[1]

        t1_left = self.turtle.xcor() - t1_width / 2
        t1_right = self.turtle.xcor() + t1_width / 2
        t1_top = self.turtle.ycor() + t1_height / 2
        t1_bottom = self.turtle.ycor() - t1_height / 2

        if (t1_left < other.turtle.xcor() + other.WIDTH and t1_right > other.turtle.xcor() and
                t1_bottom < other.turtle.ycor() and t1_top > other.turtle.ycor() - other.HEIGHT):
            return True
        return False

    def move_up(self):
        self.turtle.setheading(90)
        self.turtle.sety(self.turtle.ycor() + self.SPEED)
        self.last_move = 'up'

    def move_down(self):
        self.turtle.setheading(-90)
        self.turtle.sety(self.turtle.ycor() - self.SPEED)
        self.last_move = 'down'

    def move_right(self):
        self.turtle.setheading(0)
        self.turtle.setx(self.turtle.xcor() + self.SPEED)
        self.last_move = 'right'

    def move_left(self):
        self.turtle.setheading(180)
        self.turtle.setx(self.turtle.xcor() - self.SPEED)
        self.last_move = 'left'

    def move_back(self):
        if self.last_move == 'up':
            self.turtle.sety(self.turtle.ycor() - self.SPEED)
        elif self.last_move == 'down':
            self.turtle.sety(self.turtle.ycor() + self.SPEED)
        elif self.last_move == 'right':
            self.turtle.setx(self.turtle.xcor() - self.SPEED)
        else:
            self.turtle.setx(self.turtle.xcor() + self.SPEED)

