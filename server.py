import random
import threading
import socket

PORT = 2137
SERVER_IP = "192.168.1.3"
ADDR = (SERVER_IP, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

COLORS = [
    "red",
    "green",
    "blue",
    "orange",
    "dark goldenrod",
    "purple",
    "pink",
    "brown",
    "indigo",
    "maroon",
    "deep pink",
    "cyan",
    "magenta",
    "turquoise",
    "gold",
    "navy",
    "olive",
    "salmon",
    "teal",
    "violet"]

players_pos = {"is_end": False}
players_colors = {}
phase = "WAITING"
result = []


def handle_client(conn: socket, addr: str, player_id: int, color: str, pos: tuple[int, int]):
    print(f"{addr} (player: {player_id}) connected to server.")
    while phase == "WAITING":
        pass
    to_send = {"id": player_id, "color": color, "pos": pos, "players_colors": players_colors}
    conn.send(str(to_send).encode(FORMAT))
    connected = True
    try:
        while connected:
            message = conn.recv(2048).decode(FORMAT)
            if message is not None:
                if message == "on_finish":
                    if players_colors[player_id] not in result:
                        result.append(players_colors[player_id])
                        if len(result) + 1 >= len(players_pos):
                            players_pos["is_end"] = result
                else:
                    players_pos[player_id] = eval(message)
                conn.send(str(players_pos).encode(FORMAT))
    except:
        pass
    del players_pos[player_id]
    conn.close()
    print(f"{addr} dissconnected from server.")


def wait_to_start():
    global phase
    x = input("Press enter to start >\n")
    print("GAME started!!!")
    phase = "GAME"


def main():
    server.listen()
    print(f"Server is running and listening on {SERVER_IP}")

    wait_to_start_thread = threading.Thread(target=wait_to_start)
    wait_to_start_thread.start()

    players_cnt = 1
    while True:
        connection, address = server.accept()
        if not len(COLORS) or phase != "WAITING":
            connection.close()
            break
        pos = (random.randint(-390, -320), random.randint(265, 345))
        players_pos[players_cnt] = pos
        color = random.choice(COLORS)
        players_colors[players_cnt] = color
        COLORS.remove(color)
        thread = threading.Thread(target=handle_client, args=(connection, address, players_cnt, color, pos))
        players_cnt += 1
        thread.start()


if __name__ == "__main__":
    main()
