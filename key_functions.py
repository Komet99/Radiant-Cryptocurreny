import hashlib
import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import block
import transaction


def load_public_key(path):
    with open(path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return public_key


def load_private_key(path=None):
    if path is None:
        path = "keys/private_key.pem"
    with open(path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key


def pem_public_key_to_just_string(key):
    pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    s = str(pem.decode('utf8'))[:-27]
    res = s.replace(s[:27], '', 1)
    res.replace('\n', '')
    return res


def proof_of_work(block_hash):
    proof_no = 0
    while verifying_proof(proof_no, block_hash) is False:
        proof_no += 1
    return proof_no


def verifying_proof(proof, hash):
    # verifying the proof: does hash(last_proof, proof) contain 4 leading zeros?
    guess = f'{hash}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[:4] == "0000"


def validify_proof_number(proof_number, hash):
    guess = f'{hash}{proof_number}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    if guess_hash[:4] == "0000":
        return True
    return False



def get_block_from_json(path):
    block_file = open(path, "r").read()
    print(block_file)
    block_json = json.loads(block_file)

    index = int(block_json["index"])

    transactions_json = block_json["transactions"]
    transactions = []
    for trade in transactions_json:
        trade_dec = json.loads(trade)
        sender = trade_dec["sender"]
        receiver = trade_dec["receiver"]
        amount = trade_dec["amount"]
        date = trade_dec["time"]
        sign = trade_dec["signature"]

        t = transaction.Transaction(sender=sender, receiver=receiver, amt=amount, date=date, signature=sign)
        print(str(t))
        transactions.append(t)

    time = float(block_json["time"])

    prev = str(block_json["prev"])

    hash = str(block_json["hash"])

    final_block = block.Block(transactions, time, hash=hash)

    return final_block


def get_hashed_block_from_json(path):
    block_file = open(path, "r").read()
    print(block_file)
    block_json = json.loads(block_file)

    index = int(block_json["index"])

    transactions_json = block_json["transactions"]
    transactions = []
    for trade in transactions_json:
        trade_dec = json.loads(trade)
        sender = trade_dec["sender"]
        receiver = trade_dec["receiver"]
        amount = trade_dec["amount"]
        date = trade_dec["time"]
        sign = trade_dec["signature"]

        t = transaction.Transaction(sender=sender, receiver=receiver, amt=amount, date=date, signature=sign)
        print(str(t))
        transactions.append(t)

    time = float(block_json["time"])

    prev = str(block_json["prev"])

    hash = str(block_json["hash"])

    miner = block_json["miner"]

    proof_number = block_json["proof_number"]

    final_block = block.Block(transactions, time, hash=hash, miner=miner, proof_number=proof_number)

    return final_block

def save_pukey(public_key, filename):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)


def save_prkey(key, filename):
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)

def just_string_public_key_to_public_key(key_string):
    pem_string = "-----BEGIN PUBLIC KEY-----\n" + str(key_string) + "\n-----END PUBLIC KEY-----"
    key_bytes = pem_string.encode('utf8')
    public_key = serialization.load_pem_public_key(key_bytes)
    return public_key
