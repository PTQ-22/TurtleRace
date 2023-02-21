import threading
import socket
from collections import defaultdict

PORT = 5050
SERVER_IP = "localhost"
ADDR = (SERVER_IP, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

mapa = {}


def handle_client(conn: socket, addr, player_id):
    print(f"{addr} connected to server.")
    conn.send(str(player_id).encode(FORMAT))
    connected = True
    while connected:
        message = conn.recv(2048).decode(FORMAT)
        if message is not None:
            if str(message).strip() == "BYE":
                break
            mapa[player_id] = eval(message)
            conn.send(str(mapa).encode(FORMAT))
            print(mapa)
    conn.close()
    print(f"{addr} dissconnected from server.")


def main():
    server.listen()
    print(f"Server is running and listening on {SERVER_IP}")

    player_pos = (-360, 335)
    players_cnt = 1
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address, players_cnt))
        mapa[players_cnt] = player_pos
        players_cnt += 1
        thread.start()


if __name__ == "__main__":
    main()
