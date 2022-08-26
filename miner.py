import hashlib
import json
import simplejson
import os
import socket

import block
import transaction
import minerSetUp
from block import Block
from blockchain import Blockchain
from transaction import Transaction
import key_functions
import miner_block_distributor

buffer_size = 8192
max_amount = None

stop_updating = True


def get_miner_id(path):
    file = open(path, "r")
    return file.read().split(",")[0].split(":")[1].replace(" ", "")


def get_raw_blockfiles_list():
    blocks = []
    for block in os.listdir('minerdata/blocks'):
        blockfile = open(os.path.join('minerdata/blocks', block), "r")
        blocks.append(blockfile.read())
    return blocks


def main():
    miner_id = get_miner_id("minerdata/mining.json")
    while True:
        choice = input(
            "Hello Miner. Please Select whether to"
            "\n"
            "[1]: Receive blocks from the server or "
            "\n"
            "[2]: Solve the received blocks"
            "\n"
            "[3]: Upload the hashed (solved) blocks"
            "\n")
        choice.strip()

        if int(choice) == 1:
            print("Waiting for blocks...")
            wait_for_raw_bocks()
        if int(choice) == 2:
            print("Solving blocks... get ready for a lot of numbers")
            solve_blocks()
        if int(choice) == 3:
            print("Uploading blocks to the server")
            miner_block_distributor.connect()

        print("----------------------------------\n\n")


def wait_for_raw_bocks():
    while True:
        host_path = open("minerdata/server-address-mining.txt", "r")
        (host, port) = host_path.readlines()[0].lstrip(' ').replace('"', '').split(";")
        port = int(port)
        print("Using server: " + host)
        print("with port " + str(port))

        s = socket.socket()
        print(f"Connecting to {host}:{port}")

        s.connect((host, port))
        print("Successful connection. Waiting to receive file...")

        amount = int(s.recv(buffer_size).decode('utf8'))
        print("Got amount of blocks (" + str(amount) + ")")
        s.close()

        for index in range(amount):
            s = socket.socket()
            s.connect((host, port))
            blockfile = open("minerdata/blocks/" + str(index) + '.json', "ab")

            read_bytes = s.recv(buffer_size)
            blockfile.write(read_bytes)
            while read_bytes:
                read_bytes = s.recv(buffer_size)
                blockfile.write(read_bytes)
                print(read_bytes.decode('utf8'))
            s.close()

        '''
        # Yet again, this code used to be important when the blocks were sorted, but now it's useless
        
        s = socket.socket()
        s.connect((host, port))
        blockfile = open("minerdata/last_blockchain_block.json", "wb")

        read_bytes = s.recv(buffer_size)
        blockfile.write(read_bytes)
        while read_bytes:
            read_bytes = s.recv(buffer_size)
            blockfile.write(read_bytes)
            print(read_bytes.decode('utf8'))
        s.close()
        '''

        if stop_updating:
            print("Received all current blocks")
            s.close()
            break
    # solve_blocks()


def get_last_number_in_chain():
    last_file = open("minerdata/last_blockchain_block.json", "r")
    if last_file.read() == "Null":
        return 0
    else:
        json_f = json.load(last_file)
        return int(json_f["proof_number"])


def get_block_hash(b):
    path = os.path.join('minerdata/blocks', b + ".json")
    text = open(path, "r").read()

    block_json = json.loads(text)
    return block_json['hash']


def solve_blocks():
    # prev_number = get_last_number_in_chain()
    # Redundant code, only kept for sentimental reasons. Used to be important when the blockchain had to be sorted,
    # but I deemed that too inefficient
    sorted_proof_numbers = []
    for b in range(len(get_raw_blockfiles_list())):
        path = os.path.join('minerdata/blocks', str(b) + ".json")
        save_path = os.path.join('minerdata/hashed-blocks/')

        n = key_functions.proof_of_work(block_hash=get_block_hash(str(b)))
        # prev_number = n
        finished_block = get_block_from_json(path, n)
        finished_block.save_block(save_path)

        os.remove(path)

    print(str(n))


def get_block_from_json(path, proof_number):
    block_file = open(path)
    block_json = json.load(block_file)

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
        print(t.read_as_string())
        transactions.append(t)

    time = float(block_json["time"])

    prev = str(block_json["prev"])

    miner = key_functions.pem_public_key_to_just_string(key_functions.load_public_key("keys/public_key.pem"))

    hash = str(block_json["hash"])
    print("Block hash: " + hash)

    final_block = block.Block(transactions, time, prev=prev, hash=hash, proof_number=proof_number, miner=miner)
    print("Final block hash: " + final_block.hash)

    return final_block


main()
