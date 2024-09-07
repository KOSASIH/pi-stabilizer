import hashlib
import ecdsa
import binascii
from ecdsa.util import sigdecode_der

class PiCoin:
    def __init__(self, name, symbol, total_supply):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.blockchain = []

    def generate_genesis_block(self):
        genesis_block = {
            "index": 0,
            "previous_hash": "0" * 64,
            "transactions": [],
            "timestamp": int(time.time()),
            "nonce": 0
        }
        self.blockchain.append(genesis_block)

    def create_transaction(self, sender, recipient, amount):
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": int(time.time())
        }
        return transaction

    def add_transaction(self, transaction):
        self.blockchain[-1]["transactions"].append(transaction)

    def mine_block(self, miner):
        previous_hash = self.blockchain[-1]["previous_hash"]
        nonce = 0
        while True:
            block_hash = self.calculate_block_hash(nonce, previous_hash)
            if self.validate_proof(block_hash):
                break
            nonce += 1
        new_block = {
            "index": len(self.blockchain),
            "previous_hash": previous_hash,
            "transactions": self.blockchain[-1]["transactions"],
            "timestamp": int(time.time()),
            "nonce": nonce
        }
        self.blockchain.append(new_block)
        self.reward_miner(miner)

    def calculate_block_hash(self, nonce, previous_hash):
        block_string = str(nonce) + previous_hash + str(self.blockchain[-1]["transactions"])
        return hashlib.sha256(block_string.encode()).hexdigest()

    def validate_proof(self, block_hash):
        return block_hash[:4] == "0000"

    def reward_miner(self, miner):
        reward_transaction = self.create_transaction("PiCoin", miner, 10)
        self.add_transaction(reward_transaction)

    def get_balance(self, address):
        balance = 0
        for block in self.blockchain:
            for transaction in block["transactions"]:
                if transaction["recipient"] == address:
                    balance += transaction["amount"]
                elif transaction["sender"] == address:
                    balance -= transaction["amount"]
        return balance

class PiWallet:
    def __init__(self):
        self.private_key = ecdsa.SigningKey.from_secret_exponent(123, curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.verifying_key

    def generate_address(self):
        return binascii.hexlify(self.public_key.to_string()).decode()

    def sign_transaction(self, transaction):
        transaction_hash = hashlib.sha256(str(transaction).encode()).hexdigest()
        signature = self.private_key.sign(transaction_hash.encode())
        return signature

    def verify_transaction(self, transaction, signature, public_key):
        transaction_hash = hashlib.sha256(str(transaction).encode()).hexdigest()
        try:
            public_key.verify(signature, transaction_hash.encode())
            return True
        except:
            return False
