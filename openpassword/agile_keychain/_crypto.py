from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import os


class Crypto:
    @staticmethod
    def generate_id():
        return MD5.new(os.urandom(32)).hexdigest().upper()

    @staticmethod
    def generate_key(password, iterations):
        master_salt = os.urandom(8)
        master_key = os.urandom(1024)

        pbkdf = PBKDF2(password, master_salt, iterations)
        master_key_iv = pbkdf.read(32)
        encrypted_master_key = Crypto.encrypt(master_key_iv[0:16], master_key_iv[16:], master_key)

        validation_salt = os.urandom(8)
        validation_key_iv = Crypto.derive_key(master_key, validation_salt)
        encrypted_validation_key = Crypto.encrypt(validation_key_iv[0:16], validation_key_iv[16:], master_key)

        master = b'Salted__' + master_salt + encrypted_master_key
        validation = b'Salted__' + validation_salt + encrypted_validation_key

        return (master, validation)

    @staticmethod
    def encrypt(key, init_vector, data):
        cipher = AES.new(key, AES.MODE_CBC, init_vector)
        return cipher.encrypt(data)

    @staticmethod
    def derive_key(key, salt):
        key = key[0:-16]
        openssl_key = bytes()
        prev = bytes()
        while len(openssl_key) < 32:
            prev = MD5.new(prev + key + salt).digest()
            openssl_key += prev

        return openssl_key
