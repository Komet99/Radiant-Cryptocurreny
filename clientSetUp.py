from ast import Try
from multiprocessing import pool
from socket import socket
from warnings import catch_warnings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import json
import simplejson
import os

SERVER_ID = "127.0.0.1"
PORT = 5060
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 8192  # send 8192 bytes each time step (1KB)


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        # Standard (I have no idea about the math behind this, but I believe the python-cryptography documentation)
        key_size=2048,  # This is secure by todays standards
    )

    public_key = private_key.public_key()
    # Create File system
    # Directory
    directory = "keys"

    if not os.path.exists("keys"):
        os.mkdir(directory)
        print("Directory '% s' created" % directory)

    save_prkey(private_key, 'keys/private_key.pem')
    save_pukey(public_key, 'keys/public_key.pem')

    return public_key


def start():
    if not os.path.exists("keys/private_key.pem"):
        print("Starting initation, no finished.txt file in clientdata")
        print(
            "Hello new User! Welcome to Radiant. Let us start with generating you your public and your private key, "
            "shall we?")
        cores = int(input("Just a question... how many cores does your processor have? (Check in device-manager) \n"))
        public_key = generate_keys()
        print("Generated your public key: " + str(public_key))
        name = input(
            "To not get into legal trouble, please input your legal name in ASCII characters to commit transactions: ")
        name.encode('ASCII')

        if not os.path.exists("clientdata"):
            os.mkdir("clientdata")

        username_file = open('clientdata/username.txt', 'w')
        username_file.write(name)

    print("Get server key")
    get_server_key()

    # namefile = open('server/wallets/' + str(name) + '.json', 'w')
    # namefile.write(json.dumps({name:export_public_key_as_string(public_key)},indent=""))

    finished = open('clientdata/finished.txt', 'w')
    finished.write("Confirmed setup completion")


def get_server_key():
    s = socket()
    f = open("clientdata/server-key.json", "w")

    key_string_bytes = "".encode('utf8')
    s.connect((SERVER_ID, PORT))
    print("Established connection with server")
    parts = int.from_bytes(s.recv(BUFFER_SIZE), 'big')

    rec_bytes = s.recv(BUFFER_SIZE)

    print("Parts received as " + str(parts))

    for i in range(0,parts):
        print("Iterated loop")
        rec_bytes = s.recv(BUFFER_SIZE)
        key_string_bytes += rec_bytes

    print("Finished loop")
    print(key_string_bytes.decode('utf8'))
    f.write(json.dumps({"key": key_string_bytes.decode('utf8')}))
    f.close()


def save_prkey(key, filename):
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)


def export_public_key_as_string(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode('utf8')


def save_pukey(public_key, filename):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)


cores = 1
print("Client SetUp")
start()
