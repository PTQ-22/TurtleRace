import threading
import turtle
from turtle import Screen, Turtle
from block import Block
import socket
import ast
from player import Player

PORT = 2137
SERVER_IP = "localhost"
ADDR = (SERVER_IP, PORT)
FORMAT = "utf-8"

WIDTH = 850
HEIGHT = 750
START_GRID = (-425, 380)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

screen = Screen()
screen.setup(WIDTH, HEIGHT)
my_obj = None
connected = False


def try_to_connect():
    global connected
    client.connect(ADDR)
    connected = True


thread = threading.Thread(target=try_to_connect)
thread.start()
turtle.hideturtle()
while not connected:
    turtle.write("Błąd połączenia", align="center", font=("Verdana", 40, "normal"))
    screen.update()
screen.clear()
screen.tracer(False)


def waiting_for_id():
    global my_obj
    my_obj = client.recv(2048).decode(FORMAT)


thread = threading.Thread(target=waiting_for_id)
thread.start()
turtle.hideturtle()
while my_obj is None:
    turtle.write("Oczeiwanie na graczy", align="center", font=("Verdana", 40, "normal"))
    screen.update()
screen.clear()
screen.tracer(False)

my_data: dict = ast.literal_eval(my_obj)
my_ID = my_data['id']
player = Player(my_data['pos'], my_data['color'])
players_colors = my_data['players_colors']

screen.listen()
screen.onkeypress(player.move_up, 'Up')
screen.onkeypress(player.move_down, 'Down')
screen.onkeypress(player.move_right, 'Right')
screen.onkeypress(player.move_left, 'Left')

end_blocks = []
border_blocks = []

with open("grid.txt") as file:
    lines = file.readlines()
    y = START_GRID[1]
    for line in lines:
        x = START_GRID[0]
        for char in line:
            if char == 'X':
                border_blocks.append(Block((x, y)))
            elif char == 'e':
                end_blocks.append(Block((x, y), "green"))
            x += Block.WIDTH
        y -= Block.HEIGHT

players = {}
on_finish = False
end = False
res = []

while True:
    screen.update()
    for block in border_blocks:
        if player.is_collided_with(block):
            player.move_back()
    for end_block in end_blocks:
        if player.is_collided_with(end_block):
            on_finish = True
    if on_finish:
        client.send("on_finish".encode(FORMAT))
    else:
        client.send(str(player.turtle.pos()).encode(FORMAT))
    message = client.recv(2048).decode(FORMAT)
    d: dict = ast.literal_eval(message)
    for key, val in d.items():
        if key == "is_end":
            if val:
                end = True
                res = val
        elif key != my_ID:
            if key not in players.keys():
                players[key] = Turtle()
                players[key].shape("turtle")
                players[key].color(players_colors[key])
                players[key].penup()
            dx = players[key].xcor() - val[0]
            dy = players[key].ycor() - val[1]
            if abs(dx) > abs(dy):
                if dx < 0:
                    players[key].setheading(0)
                elif dx > 0:
                    players[key].setheading(180)
            else:
                if dy < 0:
                    players[key].setheading(90)
                elif dy > 0:
                    players[key].setheading(-90)
            players[key].setpos(val)
    if end:
        break

print("end")
# size = len(d)
screen.clear()
turtle.hideturtle()
# screen.tracer(False)
# size = 20
# end_width = 300
# end_height = 50
# end_turtle = Turtle()
# end_turtle.color("black")
# end_turtle.speed(10)
# end_turtle.hideturtle()
# end_turtle.penup()
# end_turtle.goto(-150, 380)
# end_turtle.pendown()
#
# end_turtle.begin_fill()
# for i in range(size * 2):
#     end_turtle.forward(end_width)
#     end_turtle.right(90)
#     if i % 2 == 0:
#         end_turtle.forward(end_height)
#     end_turtle.right(90)
# end_turtle.end_fill()
end_turtle = Turtle()
end_turtle.color("black")
end_turtle.speed(10)
end_turtle.hideturtle()
end_turtle.penup()
end_turtle.goto(0, 300)
end_turtle.write(f"Wyniki", align="center", font=("Verdana", 40, "bold"))
end_turtle.goto(-60, 250)
end_turtle.right(90)

for i in range(10):
    if i + 1 > len(res):
        break
    end_turtle.write(f"{i + 1}.", align="center", font=("Verdana", 20, "normal"))
    t = Turtle()
    t.shape("turtle")
    t.color(res[i])
    t.penup()
    t.goto(end_turtle.xcor() + 20, end_turtle.ycor() + 10)
    end_turtle.forward(60)
end_turtle.goto(60, 250)
for i in range(10):
    if i + 11 > len(res):
        break
    end_turtle.write(f"{i + 11}.", align="center", font=("Verdana", 20, "normal"))
    t = Turtle()
    t.shape("turtle")
    t.color(res[i])
    t.goto(end_turtle.xcor() + 20, end_turtle.ycor() + 10)
    end_turtle.forward(60)
screen.update()

turtle.exitonclick()
