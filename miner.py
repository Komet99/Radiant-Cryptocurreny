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
    print("Hello miner! ")
    print("Miner id: " + miner_id)
    wait_for_raw_bocks(miner_id)


def wait_for_raw_bocks(miner_id):
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

        if stop_updating:
            print("Retrieved all current blocks")
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
    # I know this might work another way but the json module is very hard to get to work,
    # and I am not risking anything today

    if text.lstrip() == "Null" or "":
        return ""
    else:
        with open(path) as jfile:
            print("opening " + path)
            jfile.seek(0)
            json_f = json.load(jfile)
        return str(json_f["hash"])


def solve_blocks():
    prev_number = get_last_number_in_chain()
    sorted_proof_numbers = []
    for b in range(len(get_raw_blockfiles_list())):
        path = os.path.join('minerdata/blocks', str(b) + ".json")
        save_path = os.path.join('minerdata/hashed-blocks', str(b) + ".json")
        # This may seem weird, but it's absolutely not necessary to use the same block to verify itself

        n = key_functions.proof_of_work(prev_number, get_block_hash(str(b)))
        prev_number = n
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

        t = transaction.Transaction(sender, receiver, amount, date, sign)
        print(str(t))
        transactions.append(t)

    time = float(block_json["time"])

    prev = str(block_json["prev"])

    miner = key_functions.pem_public_key_to_just_string(key_functions.load_public_key("keys/public_key.pem"))

    hash = str(block_json["hash"])
    print(hash)

    final_block = block.Block(transactions, time, prev=prev, hash=hash, proof_number=proof_number, miner=miner)
    print(final_block.hash)

    return final_block


solve_blocks()
