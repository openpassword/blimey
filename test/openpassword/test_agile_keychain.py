from nose.tools import *
import os
import openpassword


class AgileKeychainTest:
    def test_unlock_and_get_item_by_unique_id(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        fixture_path = current_path + '/../fixtures/test.agilekeychain'

        key_repository = openpassword.EncryptionKeyRepository(fixture_path)
        item_repository = openpassword.KeychainItemRepository(fixture_path)
        keychain = openpassword.Keychain(key_repository, item_repository)

        keychain.unlock("masterpassword123")
        item = keychain.get_item_by_unique_id("9E7673CCBB5B4AC9A7A8838835CB7E83")

        eq_(item.data["fields"][0]["value"], "someuser")
        eq_(item.data["fields"][1]["value"], "password123")
