from pbkdf2 import PBKDF2
from base64 import b64decode
from openpassword.exceptions import InvalidPasswordException
from openpassword.openssl_utils import derive_openssl_key
from openpassword.agilekeychain.crypto_utils import decrypt


class EncryptionKey:
    def __init__(self, key):
        self.data = b64decode(key["data"])
        self.validation = b64decode(key["validation"])
        self.iterations = key["iterations"]
        self.identifier = key["identifier"]

        self.decrypted_key = None

    def get_id(self):
        return self.identifier

    def decrypt(self, password):
        decryption_key = self._decrypt_encryption_key(password)
        validation_key = self._decrypt_validation_key(decryption_key)

        if decryption_key == validation_key:
            return decryption_key
        else:
            raise InvalidPasswordException

    def _decrypt_encryption_key(self, password):
        data_key = self._derive_password_key(password)
        return decrypt(self.data[16:], data_key)

    def _derive_password_key(self, password):
        kdf = PBKDF2(password, self.data[8:16], self.iterations)
        return kdf.read(32)

    def _decrypt_validation_key(self, decryption_key):
        validation_key = self._derive_validation_key(decryption_key)
        return decrypt(self.validation[16:], validation_key)

    def _derive_validation_key(self, decryption_key):
        return derive_openssl_key(decryption_key, self.validation[8:16])
