from nose.tools import *
import os
import openpassword


class AgileKeychainTest:
    def setUp(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        fixture_path = current_path + '/../../fixtures/test.agilekeychain'

        self.keychain = openpassword.AgileKeychain(fixture_path)

    def test_unlock_and_get_item_by_unique_id(self):
        self.keychain.unlock("masterpassword123")
        item = self.keychain.get_item_by_unique_id("9E7673CCBB5B4AC9A7A8838835CB7E83")

        eq_(item.data["fields"][0]["value"], "someuser")
        eq_(item.data["fields"][1]["value"], "password123")

    def test_search_returns_matching_items(self):
        self.keychain.unlock("masterpassword123")
        items = self.keychain.search("Folder")

        eq_(items[0].title, "Some Other Folder")
        eq_(items[1].title, "Some Folder")
