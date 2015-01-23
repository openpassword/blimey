import os
import json
import glob

from openpassword.agile_keychain.agile_keychain_item import EncryptedAgileKeychainItem


class ItemManager:
    def __init__(self, path):
        self._base_path = path

    def get_by_id(self, item_id):
        item_path = os.path.join(self._base_path, "data", "default", item_id + ".1password")

        with open(item_path, 'r') as file:
            data = json.load(file)

        return EncryptedAgileKeychainItem(data)

    def get_all_items(self):
        item_paths = glob.glob(os.path.join(self._base_path, "data", "default", "*.1password"))

        items = []
        for item_path in item_paths:
            basename = os.path.basename(item_path)
            item_id, _ = os.path.splitext(basename)
            items.append(self.get_by_id(item_id))

        return items

    def save_item(self, item):
        with open(os.path.join(self._base_path, "data", "default", "{0}.1password".format(item['uuid'])), "w") as file:
            json.dump(item, file)
