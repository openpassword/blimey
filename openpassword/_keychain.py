from openpassword.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException


class Keychain(object):
    def __init__(self, data_source):
        self.locked = True
        self._items = []
        self._data_source = data_source
        self.initialised = self._data_source.keychain_is_already_initialised()

    def unlock(self, password):
        if not self.initialised:
            raise NonInitialisedKeychainException
        self.locked = False

    def lock(self):
        self.locked = True

    def is_locked(self):
        return self.locked

    def initialise(self, password):
        if self.initialised is True:
            raise KeychainAlreadyInitialisedException

        self._data_source.initialise()
        self.initialised = True

    def is_initialised(self):
        return self.initialised

    def __iter__(self):
        return iter(self._items)
