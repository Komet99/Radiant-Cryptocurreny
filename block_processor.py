import json
import os
import shutil

from termcolor import colored

import blockchain
import transaction
from block import Block
import key_functions
import sqlite3


def process_blocks():
    db = get_database()
    cursor = db.cursor()

    pending_blocks = get_pending_blocks()
    for blk in pending_blocks:
        if validify_block(blk, db):
            print("Block valid, rewarding miner")
            reward_miner(blk)
            save_block_in_chain(blk)
        else:
            print("Could not validify block")

    # Iterate directory


def get_database():
    db = sqlite3.connect("balances.db")
    return db


def get_raw_last_block_in_chain():
    result = sorted(filter(os.path.isfile, os.listdir('block_chain')), key=os.path.getmtime)
    if len(result) < 1 or None:
        return None
    blockfile_path = os.path.join('block_chain', result[0])
    return blockfile_path


def get_last_number_in_chain(path):
    if (os.path.exists(path)):
        last_file = open(path, "r")
        if last_file.read() == "Null":
            return 0
        else:
            json_f = json.load(last_file)
            return int(json_f["proof_number"])
    else:
        return 0


def get_pending_blocks():
    pending_blocks = []
    for bo in os.listdir("pending_blocks/"):
        # check if current path is a file
        if os.path.isfile(os.path.join("pending_blocks/", bo)):
            print("Block pending...")
            if os.path.isfile(os.path.join("pending_blocks/", bo)):
                print("Current path is a file! proceeding...")
                if os.path.splitext(bo)[1] != ".json":
                    print("Extension isn't .json, removing file...")
                    os.remove(os.path.join("pending_blocks/", bo))
                    print("Removed File 1: " + os.path.join("pending_blocks/", bo))
                else:
                    try:
                        pending_blocks.append(key_functions.get_hashed_block_from_json(
                            os.path.join("pending_blocks/", bo)))
                        print("Appended block, will remove the file now")
                        os.remove(os.path.join("pending_blocks/", bo))
                    except Exception as ex:
                        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        print(message)
                        os.remove(os.path.join("pending_blocks/", bo))
                        print("Removed File 2: " + os.path.join("pending_blocks/", bo))
    return pending_blocks


def validify_block(blk, db):
    enumerate_transactions(blk)
    if blk.miner is None or blk.miner == "":
        print("No Miner")
        return False
    if blk.proof_number is None:
        print("No proof number (raw block)")
        return False
    path = get_raw_last_block_in_chain()
    if path is not None:
        prev_number = get_last_number_in_chain(path)
    else:
        prev_number = 0

    if not key_functions.validify_proof_number(proof_number=blk.proof_number, hash=blk.hash):
        print(colored("Proof number false", 'red'))
        return False
    print(colored("Proof number correct", 'green'))
    return True


reward_cash = 5


def enumerate_transactions(blk):
    db = get_database()
    for trade in blk.transactions:
        cursor = db.cursor()
        values = cursor.fetchall()
        rec_money = cursor.execute("SELECT value from balances WHERE public_key = '{trade.receiver}'", )
        # rec_balance = float(rec_money) + trade.amt
        """cursor.execute("UPDATE balances"
                       "SET value = " + ", City= 'Frankfurt'"
                                        "WHERE CustomerID = 1")
        cursor.execute("INSERT INTO balances VALUES"
                       "(" + trade.receiver + "," + trade.amt + ")")"""


def reward_miner(block):
    if not os.path.exists("pending_transactions"):
        os.mkdir("pending_transactions")
    count = 0
    # Iterate directory
    for b in os.listdir("pending_transactions"):
        # check if current path is a file
        if os.path.isfile(os.path.join("pending_transactions", b)):
            count += 1

    private_key = key_functions.load_private_key('server/keys/private_key.pem')
    public_key = key_functions.load_public_key('server/keys/public_key.pem')

    reward_transaction = transaction.Transaction(sender=key_functions.pem_public_key_to_just_string(public_key),
                                                 receiver=block.miner,
                                                 amt=reward_cash)  # Creating reward transaction

    reward_transaction.sign_transaction_rsa(private_key=private_key)  # Sign transaction with server key

    reward_transaction.saveTransaction("pending_transactions/")  # Save it to be processed soon


def save_block_in_chain(block):
    if not os.path.exists("block_chain"):
        os.mkdir("block_chain")
    block.save_block("block_chain/")
    print("Saved block in block_chain!")


try:
    cursor = sqlite3.connect("balances.db")
    cursor.execute("CREATE TABLE balances(public_key String, value Float)")
except:
    print("Database already exists / Failed to create Database")
print("Processing blocks...")
while True:
    process_blocks()
