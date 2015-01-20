import os
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import b64encode, b64decode

from openpassword.exceptions import KeyValidationException


class EncryptedKey():
    def __init__(self, key):
        self.identifier = key['identifier']
        self.level = key['level']
        self.iterations = key['iterations']
        self.data = b64decode(key['data'])
        self.validation = b64decode(key['validation'])


class DecryptedKey():
    def __init__(self, key):
        self.identifier = key['identifier']
        self.level = key['level']
        self.iterations = key['iterations']
        self.key = key['key']
