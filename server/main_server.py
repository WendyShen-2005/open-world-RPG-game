import socket
from _thread import *
import sys
from random import randint

server = "192.168.0.18"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    print(e)

s.listen(10)
print("Waiting for connection, server started")


obstacles = ""

for i in range(20):
    rand_x = randint(10, 1000)
    rand_y = randint(10, 1000)
    if i != 19:
        obstacles = obstacles + str(rand_x) + "/" + str(rand_y) + ","
    else:
        obstacles = obstacles + str(rand_x) + "/" + str(rand_y)


# tup = everyone's positions: array ["0 0", "1 1"], player = which player we are: int --> 0, 1, 2, etc
def make_pos(tup, player):
    str_pos = ""
    print("HE " + str(tup))
    for i in range(len(tup)):  # go through each of tup
        if i != player and i != len(tup) - 1:
            str_pos += str(tup[i]) + ","
        elif i != player:
            str_pos += str(tup[i])

    if str_pos == "":
        return "N/A"
    return str_pos


# stores important data that will be modified with the server client communication
pos = []


# creates a thread for each player, conn = connection stuff (don't understand yet), player = which play we're playing
def threaded_client(conn, player):
    global pos
    print(player)

    pos.append("0/0")

    # sending everyone's initial position
    conn.send(str.encode(make_pos(pos[player], player)))
    print("new player: " + str(len(pos)))
    while True:
        try:
            data = conn.recv(2048).decode()  # try to receive data from client
            # pos[player] = data

            if not data:  # shutting down server results in no more data being sent
                print("Disconnected")
                break
            elif data == "num players":
                reply = str(len(pos))
            elif data == "get obstacles":
                reply = obstacles
            else:
                pos[player] = data
                reply = make_pos(pos, player)  # format of reply: "0 0,1 1,10 100"

            print("Received: ", data)
            print("Sending: ", reply)

            conn.sendall(str.encode(reply))  # sending data back to client
        except error as e:
            print(e)
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0


while True:
    conn, addr = s.accept()  # accepts incoming connections
    # conn = what's connected, addr = ip address
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    # threading: process that runs in the background, doesn't have to wait for another function to finish first
    currentPlayer += 1

