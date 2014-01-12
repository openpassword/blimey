import json
from openpassword.keychain_item import KeychainItem
from openpassword.exceptions import InvalidUuidException


class KeychainItemRepository:

    def __init__(self, path):
        self.path = path

    def item_for_uuid(self, uuid):
        path = self._resolve_path_for_uuid(uuid)
        data = self._load_item_data(path)

        return KeychainItem(data)

    def _resolve_path_for_uuid(self, uuid):
        return self.path + '/data/default/%s.1password' % uuid

    def _load_item_data(self, path):
        try:
            file = open(path)
        except IOError:
            raise InvalidUuidException("Invalid path: %s" % path)

        data = json.load(file)
        file.close()

        return data
