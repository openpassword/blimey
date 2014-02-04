from openpassword.exceptions import InvalidPasswordException
from openpassword.exceptions import KeychainLockedException


class Keychain:

    def __init__(self, key_repository, item_repository):
        self.key_repository = key_repository
        self.item_repository = item_repository
        self._locked = True
        self._master_key = None

    def unlock(self, password, security_level="SL5"):
        master_key = self.key_repository.key_for_security_level(security_level)

        try:
            self._master_key = master_key.decrypt(password)
            self._locked = False
        except InvalidPasswordException as e:
            self._locked = True
            raise e

    def lock(self):
        self._locked = True

    def is_locked(self):
        return self._locked

    def get_item_by_unique_id(self, unique_id):
        self._check_is_locked()

        item = self.item_repository.get_item_by_unique_id(unique_id)
        item.decrypt(self._master_key)

        return item

    def search(self, query):
        self._check_is_locked()

        return self.item_repository.filter(self._get_search_function(query))

    def _get_search_function(self, query):
        def _search_callback(item):
            return item.contains(query)

        return _search_callback

    def _check_is_locked(self):
        if self.is_locked():
            raise KeychainLockedException
