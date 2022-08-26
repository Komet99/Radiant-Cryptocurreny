import json
import os
import socket

import key_functions
from key_functions import load_public_key
from key_functions import pem_public_key_to_just_string
import transaction


def main():
    print("Hello miner! ")
    if not os.path.exists("minerdata"):
        os.mkdir("minerdata")
        print("Created Minerdata")

    if not os.path.exists("minerdata/blocks"):
        os.mkdir("minerdata/blocks")
        print("Created Minerdata/blocks")

    if not os.path.exists("minerdata/hashed-blocks"):
        os.mkdir("minerdata/hashed-blocks")
        print("Created Minerdata/hashed-blocks")

    if not os.path.exists("minerdata/server-address.txt"):
        open("minerdata/server-address.txt", "w").write('127.0.0.1;5020')
        print("Created server-address.txt")

    if not os.path.exists("minerdata/server-address-mining.txt"):
        open("minerdata/server-address-mining.txt", "w").write('127.0.0.1;5030')
        print("Created server-address-mining.txt")

    if not os.path.exists("minerdata/server-address-upload.txt"):
        open("minerdata/server-address-upload.txt", "w").write('127.0.0.1;5040')
        print("Created server-address-upload.txt")

    if not os.path.exists("minerdata/mining.json"):
        mining = open("minerdata/mining.json", "w")
        print("Created mining.json")
        mining.write("{miner_id: ")
        get_miner_id()


def get_miner_id():
    print("Getting miner Id")
    hostpath = open("minerdata/server-address.txt", "r")
    (host, port) = hostpath.readlines()[0].lstrip(' ').replace('"', '').split(";")
    port = int(port)
    print("Using server: " + host)
    print("with port " + str(port))

    s = socket.socket()
    print(f"Connecting to {host}:{port}")

    s.connect((host, port))
    print("Successful connection. Waiting to receive file...")

    miner_id = ""
    f = open("minerdata/mining.json", "ab")
    # read the bytes from the file
    bytes_read = s.recv(512)
    f.write(bytes_read)
    print(bytes_read.decode('utf8'))
    # file transmitting is done
    print("Received data")
    f.close()

    print("Uploading public key to get rewards")
    public_key = load_public_key("keys/public_key.pem")
    keystring = pem_public_key_to_just_string(public_key)
    f.write(",\npublic_key: " + keystring + "}")

    s.sendall(keystring.encode('utf8'))
    print("Sent key to server")
    

    # close the socket
    s.close()
    print("Finished registration")


main()
