import os
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import b64encode, b64decode

from openpassword.exceptions import KeyValidationException


class Key:
    def __init__(self, key_object):
        self.identifier = key_object['identifier']
        self.security_level = key_object['level']
        self.iterations = key_object['iterations']
        self.data = b64decode(key_object['data'])
        self.validation = b64decode(key_object['validation'])

    def decrypt_with(self, password):
        password_key_iv = self._derive_key_from_password(password)
        master_key = Crypto.decrypt(password_key_iv[0:16], password_key_iv[16:], self.data[16:])

        validation_key_iv = self._derive_validation_key(master_key)
        validation_key = Crypto.decrypt(validation_key_iv[0:16], validation_key_iv[16:], self.validation[16:])

        if master_key != validation_key:
            raise KeyValidationException()

    @staticmethod
    def create(password, security_level, iterations):
        master_key, validation_key = Crypto.generate_key(password, iterations)

        return Key({
            'identifier': Crypto.generate_id(),
            'level': security_level,
            'iterations': iterations,
            'data': (b64encode(master_key) + b'\x00').decode('ascii'),
            'validation': (b64encode(validation_key) + b'\x00').decode('ascii'),
        })

    def _derive_key_from_password(self, password):
        key = PBKDF2(password, self.data[8:16], self.iterations)
        return key.read(32)

    def _derive_validation_key(self, encryption_key):
        return self._derive_openssl_key(encryption_key, self.validation[8:16])

    def _derive_openssl_key(self, key, salt):
        key = key[0:-16]
        openssl_key = bytes()
        prev = bytes()
        while len(openssl_key) < 32:
            prev = MD5.new(prev + key + salt).digest()
            openssl_key += prev

        return openssl_key


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
    def decrypt(key, init_vector, data):
        cipher = AES.new(key, AES.MODE_CBC, init_vector)
        return cipher.decrypt(data)

    @staticmethod
    def derive_key(key, salt):
        key = key[0:-16]
        openssl_key = bytes()
        prev = bytes()
        while len(openssl_key) < 32:
            prev = MD5.new(prev + key + salt).digest()
            openssl_key += prev

        return openssl_key
