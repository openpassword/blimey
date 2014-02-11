import os
from nose.tools import *
from openpassword.agile_keychain import KeychainItemRepository
from openpassword.exceptions import InvalidUuidException


class KeychainItemRepositoryTest:
    def setUp(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        fixture_path = current_path + '/../../../fixtures/test.agilekeychain'

        self.repository = KeychainItemRepository(fixture_path)

    def it_returns_keychain_item_for_given_unique_id(self):
        item = self.repository.item_by_unique_id('2E21D652E0754BD59F6B94B0323D0142')

        eq_(item.key_id, 'BE4CC37CD7C044E79B5CC1CC19A82A13')

    @raises(InvalidUuidException)
    def it_raises_invaliduuidexception_with_unknown_unique_id(self):
        item = self.repository.item_by_unique_id('nonexistinguuid')

    def it_returns_list_of_items_filtered_by_a_callback(self):
        def f(item):
            return "Some Folder" in item.title

        items = self.repository.filter(f)

        eq_(items[0].uuid, "D05009E62D7D401CB8ACF2FE6981C031")

    def it_return_all_items_in_the_keychain(self):
        items = self.repository.all_items()
        eq_(len(items), 9)
