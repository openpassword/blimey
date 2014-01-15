import json
from Crypto.Cipher import AES
from base64 import b64decode
from openpassword.pkcs_utils import byte_pad, strip_byte_padding
from openpassword.openssl_utils import derive_openssl_key
from os import urandom
from openpassword.crypt_utils import decrypt


class KeychainItem:
    def __init__(self, item):
        self.key_id = item["keyID"]
        self.encrypted = b64decode(item["encrypted"])
        self.data = None

    def set_private_contents(self, data):
        self.encrypted = None
        self.data = data

    def encrypt(self, original_key):
        keygen_iv = self._generate_iv()
        derived_key = self._derive_key(original_key, keygen_iv)

        data = json.dumps(self.data)
        data = byte_pad(data.encode('utf8'))
        data = self._encrypt(data, derived_key)

        self.encrypted = b''.join(['Salted__'.encode('utf8'), keygen_iv, data])

    def decrypt(self, original_key):
        keygen_iv = self.encrypted[8:16]
        derived_key = self._derive_key(original_key, keygen_iv)

        data = decrypt(self.encrypted[16:], derived_key)
        data = strip_byte_padding(data)

        self.data = json.loads(data.decode('utf8'))

    def _generate_iv(self):
        return urandom(8)

    def _derive_key(self, key, iv):
        return derive_openssl_key(key, iv)

    def _encrypt(self, data, key_iv):
        key = key_iv[0:16]
        iv = key_iv[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(data)

    def _derive_decryption_key(self, decryption_key):
        return derive_openssl_key(decryption_key, self.encrypted[8:16])
