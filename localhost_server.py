import json
import multiprocessing
import os
import shutil
import socket
import threading
import time

import tqdm
from cryptography.hazmat.primitives.asymmetric import rsa

import blockchain
import transaction
from block import Block

# device's IP address
from key_functions import save_prkey, save_pukey

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5010
# receive 1024 bytes each time
BUFFER_SIZE = 128
SEPARATOR = "<SEPARATOR>"

blockchain = blockchain.Blockchain()


# FIXME need to enumerate transactions to avoid accidentally overwriting existing ones

def set_up():
    if not os.path.exists("pending_transactions"):
        os.mkdir("pending_transactions")
        print("Created folder pending_transactions")

    if not os.path.exists("blockchain"):
        os.mkdir("blockchain")
        print("Created folder blockchain")

    if not os.path.exists("server/keys"):
        os.mkdir("server/keys")
        print("Created folder server/keys")
        create_server_wallet()
        print("Created public and private key file")

    if not os.path.exists("server/settings.json"):
        settings_file = open("server/settings.json", "w")
        settings_file.write(json.dumps({'transaction_fee': 0.05, 'miner_gain': 1}))
        settings_file.close()


def create_server_wallet():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        # Standard (I have no idea about the math behind this, but I believe the python-cryptography documentation)
        key_size=2048,  # This is secure by today's standards
    )

    public_key = private_key.public_key()

    save_prkey(private_key, 'server/keys/private_key.pem')
    save_pukey(public_key, 'server/keys/public_key.pem')

    return public_key


def accept_transactions():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    while True:
        client_socket, address = s.accept()
        client_socket.settimeout(10)
        print(f"[+] {address} is connected.")
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        uploading = True
        with open(filename, "wb") as f:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            while bytes_read:
                print(bytes_read.decode('utf8'))
                f.write(bytes_read)
                bytes_read = client_socket.recv(BUFFER_SIZE)
            print("Finished download")
            f.close()
        client_socket.close()
        shutil.move(filename, "pending_transactions/" + filename)
    print("Closed connection")

    # close the client socket
    # close the server socket
    s.close()


print("Localhost Transaction Server")
set_up()
accept_transactions()
