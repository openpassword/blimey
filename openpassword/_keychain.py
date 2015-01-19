from openpassword.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException, \
    MissingIdAttributeException, IncorrectPasswordException, KeychainLockedException


class Keychain(object):
    def __init__(self, data_source):
        self.locked = True
        self._items = {}
        self._data_source = data_source
        self.initialised = self._data_source.is_keychain_initialised()

    def unlock(self, password):
        if not self.initialised:
            raise NonInitialisedKeychainException

        self._data_source.authenticate(password)

        self.locked = False

    def lock(self):
        self.locked = True

    def is_locked(self):
        return self.locked

    def initialise(self, password, config=None):
        if self.initialised is True:
            raise KeychainAlreadyInitialisedException

        self._data_source.initialise(password, config)
        self.initialised = True

    def is_initialised(self):
        return self.initialised

    def append(self, item):
        if 'id' not in item:
            raise MissingIdAttributeException

        self._items[item['id']] = item
        self._data_source.add_item(item)

    def set_password(self, password):
        if self.locked:
            raise KeychainLockedException

        self._data_source.set_password(password)

    def __getitem__(self, item_key):
        return self._items[item_key]

    def __contains__(self, item):
        return item in self._items.values()

    def __iter__(self):
        return iter(self._items.values())
