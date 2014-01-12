import os
from nose.tools import *
from openpassword.keychain_item_repository import KeychainItemRepository


class KeychainItemRepositorySpec:

    def setUp(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        fixture_path = current_path + '/../fixtures/test.agilekeychain'

        self.repository = KeychainItemRepository(fixture_path)

    def it_returns_keychain_item_for_given_uuid(self):
        item = self.repository.item_for_uuid('2E21D652E0754BD59F6B94B0323D0142')

        eq_(item.key_id, 'BE4CC37CD7C044E79B5CC1CC19A82A13')
