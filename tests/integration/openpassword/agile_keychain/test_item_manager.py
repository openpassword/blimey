import os
import shutil
import time
import json
from nose.tools import raises

from blimey.agile_keychain._manager._item_manager import ItemManager
from blimey.agile_keychain.data_source import AgileKeychainItem
from blimey.exceptions import ItemNotFoundException


class ItemManagerTest:
    _fixture_path = os.path.join('tests', 'fixtures', 'test.agilekeychain')
    _temporary_path = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
    _password = "somepassword"

    def it_gets_items(self):
        item_manager = ItemManager(self._fixture_path)

        item = item_manager.get_by_id('5F7210FD2F3F460692B7083C60854A02')

        assert item['uuid'] == "5F7210FD2F3F460692B7083C60854A02"

    @raises(ItemNotFoundException)
    def it_throws_if_requested_item_is_not_found(self):
        item_manager = ItemManager(self._fixture_path)
        item_manager.get_by_id('notfoundid')

    def it_gets_all_items(self):
        item_manager = ItemManager(self._fixture_path)
        items = item_manager.get_all_items()

        expected_item_uuids = [
            '2E21D652E0754BD59F6B94B0323D0142',
            '4A3D784D115F4279BDFCE46D0A162D57',
            '5F7210FD2F3F460692B7083C60854A02',
            '6371E49FEFA042EDB335421459E5B29F',
            '9315F5EA8DCC4CB7BE09155DB7FCD1ED',
            '97019BEBCF9E402F8F0C033474B1B85D',
            '9E7673CCBB5B4AC9A7A8838835CB7E83',
            'B851D6E3232842B0858BC10968632A9C',
            'D05009E62D7D401CB8ACF2FE6981C031'
        ]

        assert len(items) == 9

        for item in items:
            assert item['uuid'] in expected_item_uuids

    def it_saves_items(self):
        self._init_default_data_dir()
        item_manager = ItemManager(self._temporary_path)

        item = self._get_item()
        item_manager.save_item(item)

        retrieved_item = item_manager.get_by_id(item['uuid'])

        assert item['uuid'] == retrieved_item['uuid']

    def it_sets_update_time_on_save(self):
        self._init_default_data_dir()
        item_manager = ItemManager(self._temporary_path)

        item = self._get_item()
        item_manager.save_item(item)

        retrieved_item = item_manager.get_by_id(item['uuid'])

        assert item['updatedAt'] > 0
        assert item['updatedAt'] <= time.time()

    def it_updates_contents_file_when_items_are_saved(self):
        self._init_default_data_dir()

        item_manager = ItemManager(self._temporary_path)

        item = self._get_item()
        item_manager.save_item(item)

        with open(os.path.join(self._temporary_path, 'data', 'default', 'contents.js')) as file:
            contents = json.load(file)

        assert contents[0][0] == item['uuid']
        assert contents[0][1] == item['typeName']
        assert contents[0][2] == item['title']
        assert contents[0][3] == item['locationKey']
        assert contents[0][4] == item['folderUuid']
        assert contents[0][5] == 0  # No idea what this value is
        assert contents[0][6] == 'Y'  # Corresponds to 'trashed'

    def _get_item(self):
        return AgileKeychainItem({
            'uuid': 'abcdef',
            'typeName': 'typename',
            'title': 'Title',
            'locationKey': 'locationkey',
            'folderUuid': 'undefined',
            'trashed': True
        })

    def _init_default_data_dir(self):
        os.makedirs(os.path.join(self._temporary_path, 'data', 'default'))
        self.teardown = self._path_clean

    def _path_clean(self):
        shutil.rmtree(self._temporary_path)
