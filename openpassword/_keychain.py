from openpassword.exceptions import NonInitialisedKeychainException


class Keychain(object):
    def __init__(self):
        self.locked = True
        self.initialised = True  # Generic keychain doesn't need initialisation
        self._items = []

    def unlock(self, password):
        if not self.initialised:
            raise NonInitialisedKeychainException
        self.locked = False

    def lock(self):
        self.locked = True

    def is_locked(self):
        return self.locked

    def __iter__(self):
        return iter(self._items)
