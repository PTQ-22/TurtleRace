import random
from turtle import Screen

from block import BorderBlock
from player import Player

WIDTH = 850
HEIGHT = 750
START_GRID = (-425, 380)

screen = Screen()
screen.setup(WIDTH, HEIGHT)
screen.tracer(False)

player = Player()

screen.listen()
screen.onkeypress(player.move_up, 'Up')
screen.onkeypress(player.move_down, 'Down')
screen.onkeypress(player.move_right, 'Right')
screen.onkeypress(player.move_left, 'Left')

blocks = []

with open("grid.txt") as file:
    lines = file.readlines()
    y = START_GRID[1]
    for line in lines:
        x = START_GRID[0]
        for char in line:
            if char == 'X':
                blocks.append(BorderBlock((x, y)))
            x += BorderBlock.WIDTH
        y -= BorderBlock.HEIGHT

# for i in range(5):
#     pos = (random.randint(-20, 20) * 10, random.randint(-20, 20) * 10)
#     b = BorderBlock(pos)
#     blocks.append(b)

while True:
    screen.update()
    for block in blocks:
        if player.is_collided_with(block):
            player.move_back()
