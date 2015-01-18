from openpassword.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException, \
    IncorrectPasswordException, KeychainLockedException, UnauthenticatedDataSourceException


class Keychain(object):
    def __init__(self, data_source):
        self.locked = True
        self._data_source = data_source
        self.initialised = self._data_source.is_keychain_initialised()

    def unlock(self, password):
        if not self.initialised:
            raise NonInitialisedKeychainException

        self._data_source.authenticate(password)

        self.locked = False

    def lock(self):
        self._data_source.deauthenticate()

    def is_locked(self):
        return self._data_source.is_authenticated() is False

    def initialise(self, password, config=None):
        if self.initialised is True:
            raise KeychainAlreadyInitialisedException

        self._data_source.initialise(password, config)
        self.initialised = True

    def is_initialised(self):
        return self.initialised

    def append(self, item):
        try:
            self._data_source.add_item(item)
        except UnauthenticatedDataSourceException:
            raise KeychainLockedException

    def set_password(self, password):
        if self.locked:
            raise KeychainLockedException

        self._data_source.set_password(password)

    def __getitem__(self, item_id):
        return self._data_source.get_item_by_id(item_id)

    def __contains__(self, item):
        return item in self._data_source.get_all_items()

    def __iter__(self):
        return iter(self._data_source.get_all_items())
