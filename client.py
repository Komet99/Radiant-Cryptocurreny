from fnmatch import translate
from msilib.schema import File
import main
from transaction import Transaction
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import socket
import tqdm

def start():
    open('clientdata/finished.txt', 'r')
    address_str = input("Insert path to public address of sender (as .pem file): \n")

    print("Loading recipient public key...")
    address = load_public_key(address_str)
    print("Succesfully loaded recipient public key!")

    print("Loading personal public key...")
    home_address = load_public_key("keys/public_key.pem")
    print("Succesfully loaded personal public key!")

    amount = float(input("Insert amount to transfer (can be a decimal number): \n"))

    print("Loading username...")
    username_file = open('clientdata/username.txt', 'r')
    name = username_file.readlines()[0]

    print("Calculating transaction...")
    transaction = Transaction(sender=home_address, receiver=address, amt=amount)

    input("press confirm to sign with your private key")
    private_key = load_private_key()
    transaction.signTransactionRSA(private_key)

    print("Succesfully signed transaction")
    print("Valdiating transaction...")
    if (transaction.isValidTransaction(home_address)):
        print("Transaction is valid! Congrats")
    else:
        input("Press any key to abort process")
        return False

    print("Saving transaction locally...")

    if(not os.path.exists("clientdata/transactions")):
        os.mkdir("clientdata/transactions")
    
    transaction_file = transaction.saveTransaction('clientdata/transactions')
    print("Succesfully saved transaction as json file under clientdata/transactions")

    open("clientdata/blockchain-address.txt", "wb").write("localhost\n5500")
    input("Press any key to start upload to standard blockchain. Change path in clientdata/blockchain-address, port below")

    #upload_transaction(transaction_file)


def upload_transaction(upload):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step
    
    hostpath = open("clientdata/blockchain-address.txt", "r")
    host = hostpath.readlines()[0]
    port = hostpath.readlines()[1]

    filesize = os.path.getSize(upload)


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

