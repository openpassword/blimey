from openpassword.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException, \
    IncorrectPasswordException, KeychainLockedException, UnauthenticatedDataSourceException


class Keychain(object):
    def __init__(self, data_source):
        self._data_source = data_source

    def unlock(self, password):
        self._assert_initialised()
        self._data_source.authenticate(password)

    def lock(self):
        self._data_source.deauthenticate()

    def is_locked(self):
        return self._data_source.is_authenticated() is False

    def initialise(self, password, config=None):
        self._assert_not_initialised()
        self._data_source.initialise(password, config)

    def is_initialised(self):
        return self._data_source.is_initialised()

    def append(self, item):
        try:
            self._data_source.add_item(item)
        except UnauthenticatedDataSourceException:
            raise KeychainLockedException

    def set_password(self, password):
        self._assert_not_locked()
        self._data_source.set_password(password)

    def _assert_not_locked(self):
        if self.is_locked() is True:
            raise KeychainLockedException

    def _assert_not_initialised(self):
        if self.is_initialised() is True:
            raise KeychainAlreadyInitialisedException

    def _assert_initialised(self):
        if not self.is_initialised():
            raise NonInitialisedKeychainException

    def __getitem__(self, item_id):
        self._assert_not_locked()
        return self._data_source.get_item_by_id(item_id)

    def __iter__(self):
        self._assert_not_locked()
        return iter(self._data_source.get_all_items())
