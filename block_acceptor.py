import os
import socket
from block import Block
import json

SERVER_HOST = "0.0.0.0"
MINER_PORT = 5045
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

            count = 0
            # Iterate directory
            for b in os.listdir("pending_blocks"):
                # check if current path is a file
                if os.path.isfile(os.path.join("pending_blocks", b)):
                    count += 1

            blockfile = open("pending_blocks/" + str(count + 1) + '.json', "ab")
            read_bytes = client_socket.recv(BUFFER_SIZE)
            blockfile.write(read_bytes)
            while read_bytes:
                read_bytes = client_socket.recv(BUFFER_SIZE)
                blockfile.write(read_bytes)
                print(read_bytes.decode('utf8'))
            client_socket.close()
            blockfile.close()
            print("Received block")

            print("received all blocks")

            print("Checking validity...")
            check_validity_of_block()
    # solve_blocks()


def check_validity_of_block():
    for bo in os.listdir("pending_blocks/"):
        # check if current path is a file
        if os.path.isfile(os.path.join("pending_blocks/", bo)):
            block_str = open(os.path.join("pending_blocks/", bo), "r")
            s = block_str.read()
            if s[len(s) - 1:] != "}":
                block_str.close()
                print("Removed block")
                os.remove(os.path.join("pending_blocks/", bo))


wait_for_blocks()
