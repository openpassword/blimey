from openpassword.exceptions import InvalidPasswordException


class Keychain:

    def __init__(self, key_repository, item_repository):
        self.key_repository = key_repository
        self.item_repository = item_repository
        self._locked = True

    def unlock(self, password, security_level="SL5"):
        master_key = self.key_repository.key_for_security_level(security_level)

        try:
            master_key.decrypt(password)
            self._locked = False
        except InvalidPasswordException as e:
            self._locked = True
            raise e

    def lock(self):
        self._locked = True

    def is_locked(self):
        return self._locked
