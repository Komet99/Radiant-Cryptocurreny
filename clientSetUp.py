import main
from ast import Try
from multiprocessing import pool
from warnings import catch_warnings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import json
import simplejson
import os

def generateKeys():

    private_key = rsa.generate_private_key(
    public_exponent=65537,  #Standard (I have no idea about the math behind this, but I believe the python-cryptography documentation)
    key_size=2048,          #This is secure by todays standards
    )

    public_key = private_key.public_key()
    #Create File system
    # Directory
    directory = "keys"
  
    if(not os.path.exists("keys")):
        os.mkdir(directory)
        print("Directory '% s' created" % directory)

    save_prkey(private_key, 'keys/private_key.pem')
    save_pukey(public_key, 'keys/public_key.pem')

    return public_key

def start():
    print("Starting initation, no finished.txt file in clientdata")
    print("Hello new User! Welcome to Radiant. Let us start with generating you your public and your private key, shall we?")
    cores = int(input("Just a question... how many cores does your processor have? (Check in device-manager) \n"))
    public_key = generateKeys()
    print("Generated your public key: " + str(public_key))
    name = input("To not get into legal trouble, please input your legal name in ASCII characters to commit transactions: ")
    name.encode('ASCII')

    username_file = open('clientdata/username.txt', 'w')
    username_file.write(name)

    namefile = open('server/wallets/' + str(name) + '.json', 'w')
    namefile.write(json.dumps({name:export_public_key_as_string(public_key)},indent=""))
    
    finished = open('clientdata/finished.txt', 'w')
    finished.write("Confirmed setup completion")

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
start()
