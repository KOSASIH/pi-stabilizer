import hashlib
import ecdsa
from ecdsa.util import sigdecode_der
import binascii
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class PaymentGateway:
    def __init__(self, pi_coin):
        self.pi_coin = pi_coin
        self.payment_requests = {}

    def create_payment_request(self, sender, recipient, amount):
        payment_request = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": int(time.time())
        }
        self.payment_requests[payment_request["timestamp"]] = payment_request
        return payment_request

    def process_payment(self, payment_request, private_key):
        transaction = self.pi_coin.create_transaction(payment_request["sender"], payment_request["recipient"], payment_request["amount"])
        signature = self.sign_transaction(transaction, private_key)
        self.pi_coin.add_transaction(transaction)
        self.pi_coin.mine_block("PiCoin Miner")
        return signature

    def sign_transaction(self, transaction, private_key):
        transaction_hash = hashlib.sha256(str(transaction).encode()).hexdigest()
        private_key_pem = private_key.to_pem()
        private_key_obj = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        signature = private_key_obj.sign(
            transaction_hash.encode(),
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_payment(self, payment_request, signature, public_key):
        transaction = self.pi_coin.create_transaction(payment_request["sender"], payment_request["recipient"], payment_request["amount"])
        transaction_hash = hashlib.sha256(str(transaction).encode()).hexdigest()
        public_key_pem = public_key.to_pem()
        public_key_obj = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
        try:
            public_key_obj.verify(
                signature,
                transaction_hash.encode(),
                padding.PSS(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False

class PaymentProcessor:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway

    def process_payment_request(self, payment_request, private_key):
        payment_request_signature = self.payment_gateway.process_payment(payment_request, private_key)
        return payment_request_signature

    def verify_payment_request(self, payment_request, signature, public_key):
        return self.payment_gateway.verify_payment(payment_request, signature, public_key)

class Merchant:
    def __init__(self, payment_processor, public_key):
        self.payment_processor = payment_processor
        self.public_key = public_key

    def receive_payment(self, payment_request, signature):
        if self.payment_processor.verify_payment_request(payment_request, signature, self.public_key):
            print("Payment received successfully!")
        else:
            print("Payment verification failed!")

class Customer:
    def __init__(self, payment_processor, private_key):
        self.payment_processor = payment_processor
        self.private_key = private_key

    def make_payment(self, payment_request):
        payment_request_signature = self.payment_processor.process_payment_request(payment_request, self.private_key)
        return payment_request_signature
