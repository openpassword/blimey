import json
from openpassword.keychain_item import KeychainItem
from openpassword.exceptions import InvalidUuidException


class KeychainItemRepository:

    def __init__(self, path):
        self.path = path

    def get_item_by_uuid(self, uuid):
        keychain_item_path = self._resolve_keychain_item_path(uuid)
        keychain_item = self._load_keychain_item_data(keychain_item_path)

        return KeychainItem(keychain_item)

    def _resolve_keychain_item_path(self, uuid):
        return self.path + '/data/default/%s.1password' % uuid

    def _load_keychain_item_data(self, path):
        try:
            file = open(path)
        except IOError:
            raise InvalidUuidException("Invalid path: %s" % path)

        data = json.load(file)
        file.close()

        return data
