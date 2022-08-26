import os
import socket
from block import Block
import json

SERVER_HOST = "127.0.0.1"
MINER_PORT = 5040
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 8192  # send 8192 bytes each time step (1KB)

hostpath = open("minerdata/server-address-upload.txt", "r")
(host, portstr) = hostpath.readlines()[0].lstrip(' ').replace('"', '').split(";")
port = int(portstr)


def get_hashed_blockfiles_list():
    blocks = []
    for block in os.listdir('minerdata/hashed-blocks'):
        blockfile = open(os.path.join('minerdata/hashed-blocks', block), "rb")
        blocks.append(blockfile)
    return blocks


def remove_blocklist():
    for block in os.listdir('minerdata/hashed-blocks'):
        os.remove(os.path.join('minerdata/hashed-blocks', block))


def get_raw_last_block_in_chain():
    result = sorted(filter(os.path.isfile, os.listdir('blockchain')), key=os.path.getmtime)
    if (len(result) < 1 or None):
        return None
    blockfile = open(os.path.join('blockchain', result[0]))


def connect():
    print("Miner Block Distributor")
    print("Using server: " + host)
    print("with port " + str(port))

    s = socket.socket()
    print(f"Connecting to {host}:{port}")
    s.connect((host, port))
    print("Connection established")
    blocklist = get_hashed_blockfiles_list()
    # Establishing connection
    s.settimeout(120)

    # Uploading
    upload_blocklist(blocklist, s)
    s.close()

    print("Upload finished")


def upload_blocklist(blocklist, s):
    print("Sending amount: " + str(len(blocklist)))
    s.send(str(len(blocklist)).encode('utf8'))
    s.close()
    print("Sent amount of blocks to server")
    for block in blocklist:
        print("Sending block")
        upload_block(block, s)


def upload_block(upload, s):
    if upload is None:
        print("Upload null")
        upload = "Null".encode('utf8')
        s.connect((host, port))
        s.connect()
        s.sendall(upload)

    else:
        s = socket.socket()
        s.connect((host, port))
        while True:
            # read the bytes from the file
            bytes_read = upload.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            s.sendall(bytes_read)
        print("Sent block to server")


connect()
