from nose.tools import *
from openpassword import Keychain
from openpassword.keychain_item import KeychainItem
from openpassword.exceptions import InvalidPasswordException
from openpassword.exceptions import KeychainLockedException

import fudge


class KeychainSpec:

    def it_unlocks_the_keychain_with_the_right_password(self):
        key_repository = self._unlockable_key_repository()
        item_repository = fudge.Fake('keychain_item_repository')

        keychain = Keychain(key_repository, item_repository)
        keychain.unlock('rightpassword')

        eq_(keychain.is_locked(), False)

    @raises(InvalidPasswordException)
    def it_raises_invalidpasswordexception_with_wrong_password(self):
        key = fudge.Fake('encryption_key')
        key.provides("decrypt").raises(InvalidPasswordException)

        key_repository = fudge.Fake('encryption_key_repository')
        key_repository.provides("key_for_security_level").with_args("SL5").returns(key)

        item_repository = fudge.Fake('keychain_item_repository')

        keychain = Keychain(key_repository, item_repository)
        keychain.unlock('wrongpassword')

    def it_fails_to_unlock_with_wrong_password(self):
        key = fudge.Fake('encryption_key')
        key.provides("decrypt").raises(InvalidPasswordException)

        key_repository = fudge.Fake('encryption_key_repository')
        key_repository.provides("key_for_security_level").with_args("SL5").returns(key)

        item_repository = fudge.Fake('keychain_item_repository')

        keychain = Keychain(key_repository, item_repository)
        try:
            keychain.unlock('wrongpassword')
        except InvalidPasswordException:
            pass

        eq_(keychain.is_locked(), True)

    def it_locks_when_lock_is_called(self):
        key_repository = self._unlockable_key_repository()
        item_repository = fudge.Fake('keychain_item_repository')

        keychain = Keychain(key_repository, item_repository)

        keychain.unlock('rightpassword')
        eq_(keychain.is_locked(), False)
        keychain.lock()
        eq_(keychain.is_locked(), True)

    def it_returns_an_item_by_unique_id(self):
        key_repository = self._unlockable_key_repository()

        keychain_item = fudge.Fake('keychain_item')
        item_repository = fudge.Fake('keychain_item_repository')
        item_repository.provides('get_item_by_unique_id').with_args('random_unique_id').returns(keychain_item)

        keychain = Keychain(key_repository, item_repository)
        keychain.unlock("password")

        eq_(keychain_item, keychain.get_item_by_unique_id('random_unique_id'))

    @raises(KeychainLockedException)
    def it_raises_keychainlocked_exception_when_trying_to_get_item_from_locked_keychain(self):
        key_repository = fudge.Fake('encryption_key_repository')
        item_repository = fudge.Fake('keychain_item_repository')

        keychain = Keychain(key_repository, item_repository)
        keychain.get_item_by_unique_id('some_random_item')

    def _unlockable_key_repository(self):
        key = fudge.Fake('encryption_key')
        key.provides("decrypt")

        key_repository = fudge.Fake('encryption_key_repository')
        key_repository.provides("key_for_security_level").with_args("SL5").returns(key)

        return key_repository
