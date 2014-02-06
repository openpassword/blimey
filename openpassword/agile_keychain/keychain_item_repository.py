import json
from glob import glob
from openpassword.agile_keychain.keychain_item import KeychainItem
from openpassword.exceptions import InvalidUuidException


class KeychainItemRepository:

    def __init__(self, path):
        self._path = path

    def get_item_by_unique_id(self, unique_id):
        keychain_item_path = self._resolve_keychain_item_path(unique_id)
        keychain_item_data = self._load_keychain_item_data(keychain_item_path)

        return KeychainItem(keychain_item_data)

    def filter(self, callback):
        items = []

        for path in glob(self._resolve_keychain_item_path('*')):
            keychain_item = self._load_keychain_item_data(path)
            item = KeychainItem(keychain_item)
            if callback(item):
                items.append(item)

        return items

    def _resolve_keychain_item_path(self, uuid):
        return self._path + '/data/default/{0}.1password'.format(uuid)

    def _load_keychain_item_data(self, path):
        try:
            file = open(path)
        except IOError:
            raise InvalidUuidException("Invalid path: {0}".format(path))

        data = json.load(file)
        file.close()

        return data
