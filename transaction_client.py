import key_functions
from transaction import Transaction
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import socket
import tqdm
import os


def start():
    """

    if not os.path.exists("clientdata/wallet.txt"):
        wallet = open("clientdata/wallet.txt", "w")
        wallet.write(0)

    wallet = open("clientdata/wallet.txt", "r")
    cash = float(wallet.read())

    """

    #print("You currently own a sum of " + str(cash) + " RADIANT coins")

    open('clientdata/finished.txt', 'r')
    print("Transaction Client")
    address_str = input("Welcome user! Please insert a valid path without spaces to the public address of receiver "
                        "as a .pem file: \n")

    print("Loading recipient public key...")
    address = load_public_key(address_str)
    print("Successfully loaded recipient public key!")

    print("Loading personal public key...")
    home_address = load_public_key("keys/public_key.pem")
    print("Successfully loaded personal public key!")

    amount = float(input("Insert amount to transfer (can be a decimal number): \n"))
    #if amount <= 0 or amount < cash:
    #    input("invalid amount!")
     #   return False

    print("Calculating transaction...")
    transaction = Transaction(sender=home_address, receiver=address, amt=amount)
    print(transaction)
    print("Sender: " + key_functions.pem_public_key_to_just_string(transaction.sender))
    print("Receiver: " + key_functions.pem_public_key_to_just_string(transaction.receiver))
    print("Amount: " + str(transaction.amt))

    input("press confirm to sign with your private key")
    private_key = load_private_key()
    transaction.sign_transaction_rsa(private_key)

    print("Successfully signed transaction with signature " + str(transaction.signature))
    print("Validating transaction...")
    if transaction.isValidTransaction(home_address):
        print("Transaction is valid! Congrats")
    else:
        input("Press any key to abort process")
        return False

    print("Saving transaction locally...")

    if not os.path.exists("clientdata/transactions"):
        os.mkdir("clientdata/transactions")

    if not os.path.exists("clientdata/transactions_archive"):
        os.mkdir("clientdata/transactions_archive")

    transaction_file = transaction.saveTransaction('clientdata/transactions/')
    print("Succesfully saved transaction as json file under clientdata/transactions")

    if not os.path.exists("clientdata/blockchain-address.txt"):
        open("clientdata/blockchain-address.txt", "w").write('0.0.0.0;5010')
    input(
        "Press any key to start upload to standard blockchain. Change path in clientdata/blockchain-address, "
        "port after semicolon\n")

    upload_transaction(transaction_file)


def upload_transaction(upload):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 1024  # send 1024 bytes each time step (1KB)

    hostpath = open("clientdata/blockchain-address.txt", "r")
    (host, port) = hostpath.readlines()[0].lstrip(' ').replace('"', '').split(";")
    port = int(port)
    print("Using server: " + host)
    print("with port " + str(port))

    filesize = os.path.getsize(upload)

    s = socket.socket()
    print(f"Connecting to {host}:{port}")
    s.connect((host, port))
    print("Successful connection. Sending file...")

    s.send(f"{upload}{SEPARATOR}{filesize}".encode())

    # start sending the file
    with open(upload, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            print(bytes_read.decode('utf8'))
            s.sendall(bytes_read)
            # update the progress bar
    # close the socket
    print("Finished upload, closing socket...")
    s.close()
    print("Closed socket")

    print("Moving transaction file to the archives...")

    input("Press any key to close")


def load_private_key():
    with open("keys/private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key


def load_public_key(path):
    with open(path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return public_key


start()
