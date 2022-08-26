import os

import blockchain
import transaction
from block import Block


def process_transactions():
    pending_transactions = get_pending_transactions_in_block_size()
    if pending_transactions:
        block = create_block_out_of_transactions(pending_transactions)
        share_block_for_mining(block)
        if get_pending_transactions_in_block_size():
            process_transactions()

    # Iterate directory


def create_block_out_of_transactions(transactions):
    if not os.path.exists("blockchain"):
        os.mkdir("blockchain")
    block = Block(transactions)

    return block


def get_pending_transactions_in_block_size():
    pending_transactions = []
    count = 0
    for ta in os.listdir("pending_transactions/"):
        # check if current path is a file
        if os.path.isfile(os.path.join("pending_transactions/", ta)):
            count += 1
    if count >= 4:
        print("More than 4 transactions pending...")
        for ta in os.listdir("pending_transactions/"):
            # check if current path is a file
            if os.path.isfile(os.path.join("pending_transactions/", ta)):
                print("Current path is a file! proceeding...")
                if os.path.splitext(ta)[1] != ".json":
                    print("Extension isn't .json, removing file...")
                    os.remove(os.path.join("pending_transactions/", ta))
                    print("Removed File 1: " + os.path.join("pending_transactions/", ta))
                    count -= 1
                else:
                    if len(pending_transactions) < 4 and count >= 4\
                            and os.path.exists(os.path.join("pending_transactions/", ta)):
                        try:

                            jsonfile = open(os.path.join("pending_transactions/", ta), "r")
                            transact = decode_json(jsonfile.read())
                            print("opened file")
                            jsonfile.close()

                            pending_transactions.append(transact)
                            os.remove(os.path.join("pending_transactions/", ta))

                            print("Appended to pending transactions! Size is now " + str(len(pending_transactions)))

                        except Exception:
                            print("Exception")
                            # os.remove(os.path.join("pending_transactions/", ta))
                            # print("Removed File 2: " + os.path.join("pending_transactions/", ta))
                            # count -= 1
                        if count <= 3:
                            print("Not enough pending transactions")
        return pending_transactions
    else:
        return False


def share_block_for_mining(block):
    if not os.path.exists("raw_blocks"):
        os.mkdir("raw_blocks")
    if not os.path.exists("raw_blocks/mining_data"):
        os.mkdir("raw_blocks/mining_data")
    block.save_unmined_block("raw_blocks/")

    mining_file = open("raw_blocks/mining_data.rad", "w")
    mining_file.write("block:"+block.index)


def decode_json(jsonstring):
    print("Started decoding")
    print(jsonstring)
    jsonvalues = jsonstring.replace("{", "").replace("}", "").replace(" ", "").split(",")
    sender = str(jsonvalues[0]).split(":")[1].replace('"', '')
    print("Sender: " + sender)

    receiver = str(jsonvalues[1]).split(":")[1].replace('"', '')
    print("Receiver: " + receiver)

    amount = str(jsonvalues[2]).split(":")[1].replace('"', '')
    print("Amount: " + amount)

    time = str(jsonvalues[3]).split(":")[1].replace('"', '')
    print("Time: " + time)

    signature = str(jsonvalues[4]).split(":")[1].replace('"', '')
    print("Signature: " + signature)

    print("Creating signature")

    print("Writing transaction")
    transact = transaction.Transaction(sender=sender, receiver=receiver, amt=float(amount), date=time,
                                       signature=signature)
    print(transact)
    return transact


print("Transaction Processor")
while True:
    process_transactions()
