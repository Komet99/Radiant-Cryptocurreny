import os
import stat
import sys
import hashlib
import importlib
import json
import time
from typing import Collection, KeysView
import rsa
from transaction import Transaction
from rsa.key import PrivateKey, PublicKey


class Blockchain(object):
    blockSize = 4
    def __init__(self):
        self.chain = []  # Blockchain is an array of blocks
        self.pendingTransactions = []
        self.difficulty = 4
        self.miner_rewards = 12
        self.blockSize = 4

    '''def addPendingTransaction(self, transaction, sender):
        if not transaction.sender or not transaction.receiver or not transaction.amt:
            print("Transaction Error 1: Missing sender, receiver or amt")
            return False
        if not transaction.isValidTransaction():
            print("Transaction error 2: invalid transaction");
            return False;
        self.pendingTransactions.append(transaction);
        print("Added pending transaction") # DEBUG
        return len(self.chain) + 1;'''

    def get_last_block(self):
        if (len(self.chain) > 0):
            return self.chain[-1]
        else:
            print("Error: length of chain is zero!")

    def save_chain(self, path):
        for block in self.chain:
            block.save_block(path)
        return True

    def add_block(self, block):
        if (len(self.chain) > 0):
            block.prev = self.get_last_block().hash
        else:
            block.prev = "none"
        block.index = len(self.chain)
        print("Block index is: " + str(block.index))
        if (block.index != 0):
            if (self.validate_block(block)):  # Confirms valid transaction
                self.chain.append(block)
                print("Succesfully added block with index: " + str(block.index))
        elif (block.index == 0):
            block.proof_number = 0
            self.chain.append(block)
            print("Added genesis block with index: " + str(block.index))

    def validate_block(self, block):
        if block.index > 1 and block.index != (self.chain[block.index - 1].index + 1):
            print("Block does not have right index: Is " + str(block.index) + " instead of expected: " + str(
                self.chain[block.index - 1].index + 1))
            return False
        if (block.proof_number):
            print("Succesfully mined block")
            return True

    def getBlock(self, index):
        return self.chain[index]
