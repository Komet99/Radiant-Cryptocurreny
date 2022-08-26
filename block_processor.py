import json
import os

import blockchain
import transaction
from block import Block
import key_functions


def process_blocks():
    print("Processing transactions")
    pending_blocks = get_pending_blocks
    for blk in pending_blocks:
        if validify_block(blk):
            reward_miner(blk)
            save_block_in_chain(blk)
    process_blocks()

    # Iterate directory


def get_raw_last_block_in_chain():
    result = sorted(filter(os.path.isfile, os.listdir('blockchain')), key=os.path.getmtime)
    if (len(result) < 1 or None):
        return None
    blockfile_path = os.path.join('blockchain', result[0])


def get_last_number_in_chain(path):
    last_file = open(path, "r")
    if last_file.read() == "Null":
        return 0
    else:
        json_f = json.load(last_file)
        return int(json_f["proof_number"])


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
                    os.remove(os.path.join("pending_transactions/", bo))
                    print("Removed File 1: " + os.path.join("pending_transactions/", bo))
                else:
                    try:
                        pending_blocks.append(key_functions.get_block_from_json(
                            os.path.join("pending_transactions/", bo)))
                        print("Appended block")
                    except Exception:
                        print("Exception")
                        os.remove(os.path.join("pending_transactions/", bo))
                        print("Removed File 2: " + os.path.join("pending_transactions/", bo))
    return pending_blocks


def validify_block(blk):
    if blk.miner is None:
        return False
    if blk.proof_number is None:
        return False
    path = get_raw_last_block_in_chain()
    prev_number = get_last_number_in_chain(path)

    if not key_functions.validify_proof_number(prev_hash=blk.prev, proof_number=blk.proof_number, hash=blk.hash,
                                               last_proof=prev_number):
        return False

    return True

reward_cash = 5

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

    reward_transaction = transaction.Transaction(public_key, block.miner, amt=reward_cash)  # Creating reward transaction

    reward_transaction.sign_transaction_rsa(private_key=private_key) # Sign transaction with server key

    reward_transaction.saveTransaction("pending_transactions/" + str(count) + ".json") # Save it to be processed soon


def save_block_in_chain(block):
    if not os.path.exists("blockchain"):
        os.mkdir("blockchain")
    block.save_block("blockchain")


while True:
    process_blocks()
