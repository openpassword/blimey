import os
import shutil
from openpassword.agile_keychain._item_manager import ItemManager
from openpassword.agile_keychain.agile_keychain_item import DecryptedItem
from nose.tools import raises

# from openpassword.exceptions import KeyAlreadyExistsForLevelException, InvalidKeyFileException
# from openpassword.agile_keychain._key import Key


class ItemManagerTest:
    _fixture_path = os.path.join('tests', 'fixtures', 'test.agilekeychain')
    _temporary_path = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
    _password = "somepassword"

    def it_gets_items(self):
        item_manager = ItemManager(self._fixture_path)

        item = item_manager.get_by_id('5F7210FD2F3F460692B7083C60854A02')

        assert item['uuid'] == "5F7210FD2F3F460692B7083C60854A02"

    def it_saves_items(self):
        self._init_default_data_dir()
        item_manager = ItemManager(self._temporary_path)

        item = DecryptedItem.create()
        item_manager.save_item(item)

        retrieved_item = item_manager.get_by_id(item['uuid'])

        assert item['uuid'] == retrieved_item['uuid']

    def _init_default_data_dir(self):
        os.makedirs(os.path.join(self._temporary_path, 'data', 'default'))
        self.teardown = self._path_clean

    def _path_clean(self):
        shutil.rmtree(self._temporary_path)
