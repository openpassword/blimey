import os
import json

from openpassword.agile_keychain.agile_keychain_item import EncryptedItem


class ItemManager:
    def __init__(self, path):
        self._base_path = path

    def get_by_id(self, item_id):
        item_path = os.path.join(self._base_path, "data", "default", item_id + ".1password")

        with open(item_path, 'r') as file:
            data = json.load(file)

        return EncryptedItem(data)

    def save_item(self, item):
        with open(os.path.join(self._base_path, "data", "default", "{0}.1password".format(item['uuid'])), "w") as file:
            json.dump(item, file)

        # key = self._get_key_for_item(data)

        # encrypted = b64decode(data['encrypted'])
        # init_vector = encrypted[8:16]
        # derived_key = Crypto.derive_key(key.decrypted_key, init_vector)
        # decrypted = Crypto.decrypt(derived_key[0:16], derived_key[16:], encrypted[16:])
        # decrypted = strip_byte_padding(decrypted)
        # decrypted_data = json.loads(decrypted.decode('ascii'))

        # item = AgileKeychainItem()
        # item.id = data['uuid']
        # item.secrets = decrypted_data

        # return item
