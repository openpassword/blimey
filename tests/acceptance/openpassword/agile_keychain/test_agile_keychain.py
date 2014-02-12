import os
import pickle

from nose.tools import *
from nose import SkipTest

import openpassword
from openpassword.item_collection import ItemCollection


def skip(f):
    """ Decorator to indicate a test should be skipped."""
    def g(*args, **kw):
        raise SkipTest()
    return make_decorator(f)(g)


class AgileKeychainTest:
    def setUp(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        fixture_path = current_path + '/../../../fixtures/test.agilekeychain'

        self.keychain = openpassword.AgileKeychain(fixture_path)

    def test_unlock_keychain(self):
        eq_(self.keychain.is_locked(), True)
        self.keychain.unlock("masterpassword123")

        eq_(self.keychain.is_locked(), False)

    def test_get_item_by_unique_id(self):
        self.keychain.unlock("masterpassword123")
        item = self.keychain.get_item_by_unique_id("97019BEBCF9E402F8F0C033474B1B85D")

        eq_(item.data["fields"][0]["value"], "somedifferentusername")
        eq_(item.data["fields"][1]["value"], "password123")

    def test_get_all_items_returns_collection_of_9_items_for_a_9_item_keychain(self):
        self.keychain.unlock("masterpassword123")
        all_items = self.keychain.all_items()
        eq_(type(all_items), ItemCollection)
        eq_(len(all_items), 9)

    def test_lock_keychain(self):
        eq_(self.keychain.is_locked(), True)
        self.keychain.unlock("masterpassword123")

        eq_(self.keychain.is_locked(), False)
        self.keychain.lock()
        eq_(self.keychain.is_locked(), True)

