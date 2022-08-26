import array
import os
import stat
import sys
import hashlib
import importlib
import json
import time
from typing import KeysView
from cryptography.hazmat.primitives.asymmetric import rsa
from transaction import Transaction


class Block(object):
    def __init__(self, transactions, creation_time=time.time(), prev=None, hash=None, proof_number=None, miner=None):

        self.transactions = []
        self.index = 0  # Index of block
        self.transactions = transactions  # Stored transactions
        self.time = creation_time  # Time of block creation

        if prev is None:        # Hash of previous block, empty if genesis block
            self.prev = ''      # Make it empty
        else:
            self.prev = prev    # Fill in previous blocks hash

        if hash is None:
            self.hash = self.calculate_hash()  # Hash of block
        else:
            self.hash = hash

        if proof_number is None:
            self.proof_number = 0
        else:
            self.proof_number = proof_number

        if miner is None:
            self.miner = ""
        else:
            self.miner = miner

    def calculate_hash(self):
        hash_transactions = ""
        for transaction in self.transactions:
            hash_transactions += transaction.hash
        hash_string = str(self.time) + hash_transactions + self.prev + str(self.index)
        hash_encoded = json.dumps(hash_string, sort_keys=True).encode()
        return hashlib.sha256(hash_encoded).hexdigest()

    def save_block(self, path):
        if not os.path.exists(path):
            transactions = []
            for transaction in self.transactions:
                transactions.append(str(transaction.export_as_json()))
            json_string = json.dumps(
                {
                    "index":           self.index,
                    "transactions":    transactions,
                    "time":            self.time,
                    "prev":            self.prev,
                    "hash":            self.hash,
                    "proof_number":    self.proof_number,
                    "miner":           self.miner
                })
            save_file = open(path, "w")
            save_file.write(json_string)
            save_file.close()

    def save_unmined_block(self, path):
        if not os.path.exists(path + "self.index"):
            transactions = []
            for transaction in self.transactions:
                transactions.append(str(transaction.export_as_json()))

            count = 0
            # Iterate directory
            for b in os.listdir(path):
                # check if current path is a file
                if os.path.isfile(os.path.join(path, b)):
                    count += 1

            json_string = json.dumps(
                {"index": count,
                 "transactions": transactions,
                 "time": self.time,
                 "prev": self.prev,
                 "hash": self.hash})

            save_file = open(path + str(count + 1) + ".json", "w")
            save_file.write(json_string)
            save_file.close()
