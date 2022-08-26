import os
import socket

import key_functions
from block import Block
import json

SERVER_HOST = "0.0.0.0"
PORT = 5060
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 8192  # send 8192 bytes each time step (1KB)


def get_server_key():
    return key_functions.load_public_key("server/keys/public_key.pem")


def connect():
    print("Server Key Distributor")
    s = socket.socket()
    s.bind((SERVER_HOST, PORT))

    print("Hosting server with ip " + SERVER_HOST + " on port " + str(PORT))
    s.listen()
    public_key_string = key_functions.pem_public_key_to_just_string(get_server_key())
    while True:
        # Establishing connection
        print(f"[*] Listening as {SERVER_HOST}:{PORT}")
        client_socket, address = s.accept()
        client_socket.settimeout(120)
        print("Established connection with " + str(address))
        upload_key(public_key_string, client_socket)
        # Uploading


def upload_key(upload, client_socket):
    str(upload)
    print("Uploading key")
    # read the bytes from the file
    upload_bytes = upload.encode('utf8')
    upload_bytes_len = len(upload_bytes)
    print("upload byte length is: " + str(upload_bytes_len))

    parts = int(upload_bytes_len / BUFFER_SIZE)
    print("parts is: " + str(parts))
    if(parts < 1):
        parts = 1
        print("Corrected parts to 1. Parts = " + str(parts))
    string_len = len(upload)
    client_socket.sendall(parts.to_bytes(10, 'big'))

    for i in range(parts):
        bytes_read = upload[parts * i:int(string_len / parts)].encode('utf8')
        print(bytes_read.decode('utf8'))
        client_socket.sendall(bytes_read)

    print("Sent key to miner")

connect()
