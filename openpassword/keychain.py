from openpassword.exceptions import InvalidPasswordException


class Keychain:

    def __init__(self, encryption_key):
        self.encryption_key = encryption_key
        self._locked = True

    def unlock(self, password):
        try:
            self.encryption_key.decrypt(password)
            self._locked = False
        except InvalidPasswordException as e:
            self._locked = True
            raise(e)

    def lock(self):
        self._locked = True

    def is_locked(self):
        return self._locked
