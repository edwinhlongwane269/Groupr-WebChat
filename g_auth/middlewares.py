from cryptography.fernet import Fernet, MultiFernet
from cryptography.x509 import random_serial_number

# Generate encrtyption keys
encryption_key_1 = Fernet(Fernet.generate_key())
encryption_key_2 = Fernet(Fernet.generate_key())

class GCipher:
    def __init__(self, key1, key2, blk_lz):
        self.key1 = key1
        self.key2 = key2
        self.blk_lz = blk_lz

    def encrypt(self, request):
        # Encrypt the request with the first key
        request = self.key1.encrypt(request)
        # Encrypt the request with the second key
        request = self.key2.encrypt(request)
        # Encrypt the request with the block length
        request = self.blk_lz.encrypt(request)
        return request