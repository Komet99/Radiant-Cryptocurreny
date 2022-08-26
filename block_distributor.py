import os
import socket
from block import Block
import json

SERVER_HOST = "0.0.0.0"
MINER_PORT = 5030
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 8192  # send 8192 bytes each time step (1KB)


def get_raw_blockfiles_list():
    blocks = []
    for block in os.listdir('raw_blocks'):
        blockfile = open(os.path.join('raw_blocks', block), "rb")
        blocks.append(blockfile)
    return blocks

def get_raw_last_block_in_chain():
    result = sorted(filter(os.path.isfile, os.listdir('blockchain')), key=os.path.getmtime)
    if (len(result) < 1 or None):
        return None
    blockfile = open(os.path.join('blockchain',result[0]))


def connect():
    print("Starting server")
    s = socket.socket()
    s.bind((SERVER_HOST, MINER_PORT))

    print("Hosting server with ip " + SERVER_HOST + " on port " + str(MINER_PORT))
    s.listen()
    blocklist = get_raw_blockfiles_list()
    while True:
        # Establishing connection
        print(f"[*] Listening as {SERVER_HOST}:{MINER_PORT}")
        client_socket, address = s.accept()
        client_socket.settimeout(120)

        # Uploading
        upload_blocklist(blocklist, client_socket, s)
        upload_block(get_raw_last_block_in_chain(), s)
        client_socket.close()
        blocklist = get_raw_blockfiles_list()


def upload_blocklist(blocklist, client_socket, s):
    client_socket.send(str(len(blocklist)).encode('utf8'))
    client_socket.close()
    print("Sent amount of blocks to miner")
    for block in blocklist:
        upload_block(block, s)


def upload_block(upload, s):
    if upload is None:
        upload = ("Null").encode('utf8')
        client_socket, address = s.accept()
        client_socket.sendall(upload)

    else:
        client_socket, address = s.accept()
        while True:
            # read the bytes from the file
            bytes_read = upload.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            client_socket.sendall(bytes_read)
        print("Sent block to miner")


connect()
