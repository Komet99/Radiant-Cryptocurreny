import time
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import exceptions
import key_functions
import json
import time
import urllib
import os


class Transaction(object):
    def __init__(self, sender, receiver, amt, date=None, hash=None, signature=None):
        if type(sender) is rsa.RSAPublicKey:
            self.sender = self.pem_public_key_to_just_string(sender)
        else:
            self.sender = sender
        if type(receiver) is rsa.RSAPublicKey:
            self.receiver = self.pem_public_key_to_just_string(receiver)
        else:
            self.receiver = receiver
        self.amt = amt

        if date is None:
            self.date = time.time()
        else:
            self.date = date

        if hash is None:
            self.hash = self.calculate_hash()
        else:
            self.hash = hash

        if signature:
            self.signature = signature

    def calculate_hash(self):
        hashString = key_functions.pem_public_key_to_just_string(self.sender) + key_functions.pem_public_key_to_just_string(self.receiver) + str(self.amt) + str(self.date)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()

    def sign_transaction_rsa(self, private_key):
        hashEncoded = json.dumps(
            {"sender": str(self.sender), "receiver": str(self.receiver), "amount": self.amt, "time": self.date},
            sort_keys=True).encode('utf8')  # dumps values in json file
        hashf = hashlib.sha256(hashEncoded).hexdigest().encode(
            'utf8')  # transforms bytes into hex bytes after encrypting them
        signature = private_key.sign(hashf,
                                     padding.PSS(
                                         mgf=padding.MGF1(hashes.SHA256()),
                                         salt_length=padding.PSS.MAX_LENGTH),
                                     hashes.SHA256())
        self.signature = signature
        return signature

    def read_transaction_rsa(self, public_key):
        hash_encoded = json.dumps(
            {"sender": str(self.sender), "receiver": str(self.receiver), "amount": self.amt, "time": self.date},
            sort_keys=True).encode('utf8')
        hashf = hashlib.sha256(hash_encoded).hexdigest().encode('utf8')
        print("Trying verification")
        try:
            public_key.verify(
                self.signature, hashf, padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256())
            return True
        except exceptions.InvalidSignature:
            print("False signature Exception")
        except Exception:
            print("Any other exception, but not a signature exception")

    def isValidTransaction(self, public_key):
        if self.sender == self.receiver:
            return False
        if self.sender == "Miner Rewards":
            return True
        if not self.signature or len(self.signature) == 0:
            print("No Signature!")
            return False
        if not self.read_transaction_rsa(public_key):
            print("Verifying signature...")
            return False
        return True

    def saveTransaction(self, path):
        jsonfile = json.dumps(
            {"sender": str(self.sender), "receiver": str(self.receiver), "amount": self.amt, "time": self.time,
             "signature": str(self.signature)})
        count = 0
        # Iterate directory
        for w in os.listdir(path):
            # check if current path is a file
            if os.path.isfile(os.path.join(path, w)):
                count += 1

        fullfilename = str(path + "transaction" + str(count + 1) + ".json")
        tfile = open(fullfilename, "w")
        tfile.write(jsonfile)
        return fullfilename

    def export_as_json(self):
        jsonfile = json.dumps(
            {"sender": str(self.sender), "receiver": str(self.receiver), "amount": self.amt, "time": self.time,
             "signature": str(self.signature)}, sort_keys=True)
        return jsonfile

    @staticmethod
    def pem_public_key_to_just_string(self, key):
        pem = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        s = str(pem.decode('utf8'))[:-27]
        res = s.replace(s[:27], '', 1)
        res.replace('\n', '')
        print(res)
        return res

    @staticmethod
    def pem_private_key_to_just_string(self, key):
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL
        )
        s = str(pem.decode('utf8'))[:-27]
        res = s.replace(s[:27], '', 1)  # Cuts off the pem stuff
        res.replace('\n', '')
        print(res)
        return res
