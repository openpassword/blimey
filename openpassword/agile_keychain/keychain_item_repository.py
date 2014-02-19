import json
from glob import glob
import os

from openpassword.agile_keychain.keychain_item import KeychainItem
from openpassword.exceptions import InvalidPathException
from openpassword import abstract
from openpassword.item_collection import ItemCollection
from openpassword.data_object import MetaItem


class KeychainItemRepository(abstract.KeychainItemRepository):

    def __init__(self, path):
        self._path = path

    def item_by_unique_id(self, unique_id):
        keychain_item_path = self._resolve_keychain_item_path(unique_id)
        keychain_item_data = self._load_keychain_item_data(keychain_item_path)

        return KeychainItem(keychain_item_data)

    def all_items(self):
        items = []

        for path in glob(self._resolve_keychain_item_path('*')):
            keychain_item_data = self._load_keychain_item_data(path)
            keychain_item_data['unique_id'] = keychain_item_data['uuid']
            item = MetaItem(keychain_item_data)
            items.append(item)

        return ItemCollection(items)

    def _resolve_keychain_item_path(self, uuid):
        return os.path.join(self._path, 'data', 'default', "{0}.1password".format(uuid))

    def _load_keychain_item_data(self, path):
        try:
            file = open(path)
        except IOError:
            raise InvalidPathException("Invalid path: {0}".format(path))

        data = json.load(file)
        file.close()

        return data
