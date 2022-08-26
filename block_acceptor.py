import os
import socket
from block import Block
import json

SERVER_HOST = "0.0.0.0"
MINER_PORT = 5040
BUFFER_SIZE = 8192  # send 8192 bytes each time step (1KB)


def wait_for_blocks():
    if not os.path.exists("pending_blocks"):
        os.mkdir("pending_blocks")
    s = socket.socket()
    s.bind((SERVER_HOST, MINER_PORT))
    print(f"Hosting server at {SERVER_HOST}:{MINER_PORT}")
    while True:
        s.listen()
        print("Waiting for new connection")
        client_socket, address = s.accept()
        print("Accepted connection with " + str(address))

        amount = int(client_socket.recv(BUFFER_SIZE).decode('utf8'))

        print("Got amount of blocks (" + str(amount) + ")")
        client_socket.close()

        for index in range(amount):
            client_socket, address = s.accept()

            blockfile = open("pending_blocks/" + str(index) + '.json', "ab")
            read_bytes = client_socket.recv(BUFFER_SIZE)
            blockfile.write(read_bytes)
            while read_bytes:
                read_bytes = client_socket.recv(BUFFER_SIZE)
                blockfile.write(read_bytes)
                print(read_bytes.decode('utf8'))
            client_socket.close()
            print("Received block")

            print("received all blocks")
    # solve_blocks()

wait_for_blocks()
