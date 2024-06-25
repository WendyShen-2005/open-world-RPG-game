import socket
from _thread import *
import sys
from random import randint
import pickle

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
def other_player_data(players_list, active_player_index):
    return_list = []
    for i in range(len(players_list)):
        if i != active_player_index:
            return_list.append(players_list[i])

    return return_list


# stores important data that will be modified with the server client communication
all_players = []


# creates a thread for each player, conn = connection stuff (don't understand yet), player = which play we're playing
def threaded_client(conn, player):
    global pos
    print(player)

    all_players.append([(0,0), []])
    # pos.append("0/0")

    # sending everyone's initial position
    conn.send(pickle.dumps("hello"))
    print("new player: " + str(len(all_players)))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))  # try to receive data from client

            if not data:  # shutting down server results in no more data being sent
                print("Disconnected")
                break
            elif data == "get obstacles":
                reply = obstacles
            else:
                all_players[player] = data
                reply = other_player_data(all_players, player)  # format of reply: "0 0,1 1,10 100"

            print("Received: ", data)
            print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))  # sending data back to client
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

