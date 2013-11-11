from openpassword.exceptions import InvalidPasswordException

import time


class Keychain:

    def __init__(self, encryption_key, timeout=60):
        self.encryption_key = encryption_key
        self._locked = True
        self._timeout = timeout
        self._timestamp = None

    def unlock(self, password):
        try:
            self.encryption_key.decrypt(password)
            self._timestamp = time.time()
            self._locked = False
        except InvalidPasswordException as e:
            self._locked = True
            raise(e)

    def is_locked(self):
        return self._locked or (self._timestamp + self._timeout <= time.time())
