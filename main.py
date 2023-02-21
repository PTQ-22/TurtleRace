from turtle import Screen, Turtle
from block import BorderBlock
import socket
import ast
from player import Player

PORT = 5050
SERVER_IP = "localhost"
ADDR = (SERVER_IP, PORT)
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
my_ID = int(client.recv(2048).decode(FORMAT))

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

players = {}

while True:
    screen.update()
    for block in blocks:
        if player.is_collided_with(block):
            player.move_back()

    client.send(str(player.turtle.pos()).encode(FORMAT))
    message = client.recv(2048).decode(FORMAT)
    d: dict = ast.literal_eval(message)
    for key, val in d.items():
        if key != my_ID:
            if key not in players.keys():
                players[key] = Turtle()
                players[key].shape("turtle")
                players[key].color("green")
                players[key].penup()
            dx = players[key].xcor() - val[0]
            dy = players[key].ycor() - val[1]
            if abs(dx) > abs(dy):
                if dx < 0:
                    players[key].setheading(0)
                    print("XXXX")
                elif dx > 0:
                    players[key].setheading(180)
            else:
                if dy < 0:
                    players[key].setheading(90)
                elif dy > 0:
                    players[key].setheading(-90)
            players[key].setpos(val)

    # print(players)
