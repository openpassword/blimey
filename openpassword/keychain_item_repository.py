import json
from openpassword.keychain_item import KeychainItem


class KeychainItemRepository:

    def __init__(self, path):
        self.path = path

    def item_for_uuid(self, uuid):
        item_file = open(self.path + '/data/default/%s.1password' % uuid)
        data = json.load(item_file)
        item_file.close()

        return KeychainItem(data)
