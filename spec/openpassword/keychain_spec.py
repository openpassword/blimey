from nose.tools import *
import nose

from openpassword._keychain import Keychain
from openpassword.exceptions import NonInitialisedKeychainException
from spec.openpassword.fudge_wrapper import getMock


class KeychainSpec:
    def it_is_created_locked(self):
        keychain = Keychain()
        eq_(keychain.is_locked(), True)

    def it_unlocks_the_keychain_with_the_right_password(self):
        keychain = Keychain()
        keychain.unlock('rightpassword')
        eq_(keychain.is_locked(), False)

    def it_is_iterable_as_list_of_items_when_unlocked(self):
        keychain = Keychain()
        keychain.unlock("righpassowrd")

        try:
            iter(keychain)
        except TypeError:
            raise AssertionError("Keychain is not iterable")

    def it_locks_the_keychain(self):
        keychain = Keychain()
        keychain.unlock('rightpassword')
        eq_(keychain.is_locked(), False)

        keychain.lock()
        eq_(keychain.is_locked(), True)

    @raises(NonInitialisedKeychainException)
    def it_raises_NonInitialisedKeychainException_when_unlocking_uninitialized_keychain(self):
        keychain = Keychain()
        keychain.initialised = False
        keychain.unlock("somepassword")
