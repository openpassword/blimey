from Crypto.Cipher import AES
from base64 import b64decode
import json
from openpassword.pksc_utils import strip_byte_padding
from openpassword.openssl_utils import derive_openssl_key


class KeychainItem:
    def __init__(self, item):
        self.encrypted = b64decode(item["encrypted"])

    def decrypt(self, decryption_key):
        key = self._derive_decryption_key(decryption_key)
        data = self._decrypt(self.encrypted[16:], key)

        data = strip_byte_padding(data)

        return json.loads(data.decode('utf8'))

    def _derive_decryption_key(self, decryption_key):
        return derive_openssl_key(decryption_key, self.encrypted[8:16])

    def _decrypt(self, data, key_iv):
        key = key_iv[0:16]
        iv = key_iv[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.decrypt(data)
