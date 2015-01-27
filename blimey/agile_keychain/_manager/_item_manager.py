import os
import json
import glob
import time

from blimey.agile_keychain.agile_keychain_item import EncryptedAgileKeychainItem
from blimey.exceptions import ItemNotFoundException


class ItemManager:
    def __init__(self, path):
        self._base_path = path

    def get_by_id(self, item_id):
        item_path = os.path.join(self._base_path, "data", "default", item_id + ".1password")

        try:
            with open(item_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise ItemNotFoundException

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
        item['updatedAt'] = int(time.time())

        with open(os.path.join(self._base_path, "data", "default", "{0}.1password".format(item['uuid'])), "w") as file:
            json.dump(item, file)

        self._update_contents_file()

    def _update_contents_file(self):
        item_paths = glob.glob(os.path.join(self._base_path, "data", "default", "*.1password"))

        contents = []
        for item_path in item_paths:
            basename = os.path.basename(item_path)
            item_id, _ = os.path.splitext(basename)
            item = self.get_by_id(item_id)

            contents.append([
                item['uuid'],
                item['typeName'],
                item['title'],
                item['locationKey'],
                item['folderUuid'],
                0,
                'Y' if item['trashed'] is True else 'N'
            ])

        with open(os.path.join(self._base_path, "data", "default", "contents.js"), "w") as file:
            json.dump(contents, file)
