from nose.tools import *
from openpassword import Keychain
from openpassword.keychain_item import KeychainItem
from openpassword import EncryptionKey
from openpassword import EncryptionKeyRepository
from openpassword import KeychainItemRepository
from openpassword.exceptions import InvalidPasswordException
from openpassword.exceptions import KeychainLockedException

import fudge
from spec.openpassword.fudge_wrapper import getMock


class KeychainSpec:
    def it_unlocks_the_keychain_with_the_right_password(self):
        encryption_key = self._encryption_key_that_provides_decrypt()
        encryption_key_repository = self._encryption_key_repository_that_returns_key(encryption_key)
        keychain_item_repository = getMock(KeychainItemRepository)

        keychain = Keychain(encryption_key_repository, keychain_item_repository)
        keychain.unlock('rightpassword')

        eq_(keychain.is_locked(), False)

    @raises(InvalidPasswordException)
    def it_raises_invalidpasswordexception_with_wrong_password(self):
        encryption_key = self._encryption_key_that_raises_invalid_password_exception()
        encryption_key_repository = self._encryption_key_repository_that_returns_key(encryption_key)
        keychain_item_repository = getMock(KeychainItemRepository)

        keychain = Keychain(encryption_key_repository, keychain_item_repository)
        keychain.unlock('wrongpassword')

    def it_fails_to_unlock_with_wrong_password(self):
        encryption_key = self._encryption_key_that_raises_invalid_password_exception()
        encryption_key_repository = self._encryption_key_repository_that_returns_key(encryption_key)
        keychain_item_repository = getMock(KeychainItemRepository)

        keychain = Keychain(encryption_key_repository, keychain_item_repository)
        try:
            keychain.unlock('wrongpassword')
        except InvalidPasswordException:
            pass

        eq_(keychain.is_locked(), True)

    def it_locks_when_lock_is_called(self):
        encryption_key = self._encryption_key_that_provides_decrypt()
        encryption_key_repository = self._encryption_key_repository_that_returns_key(encryption_key)
        keychain_item_repository = getMock(KeychainItemRepository)

        keychain = Keychain(encryption_key_repository, keychain_item_repository)

        keychain.unlock('rightpassword')
        eq_(keychain.is_locked(), False)
        keychain.lock()
        eq_(keychain.is_locked(), True)

    def it_returns_an_item_by_unique_id(self):
        encryption_key = self._encryption_key_that_provides_decrypt()
        encryption_key_repository = self._encryption_key_repository_that_returns_key(encryption_key)

        keychain_item = getMock(KeychainItem)
        keychain_item_repository = getMock(KeychainItemRepository)
        keychain_item_repository.provides('get_item_by_unique_id').with_args('random_unique_id').returns(keychain_item)

        keychain = Keychain(encryption_key_repository, keychain_item_repository)
        keychain.unlock("password")

        eq_(keychain_item, keychain.get_item_by_unique_id('random_unique_id'))

    @raises(KeychainLockedException)
    def it_raises_keychainlocked_exception_when_trying_to_get_item_from_locked_keychain(self):
        key_repository = fudge.Fake('encryption_key_repository')
        item_repository = fudge.Fake('keychain_item_repository')

        keychain = Keychain(key_repository, item_repository)
        keychain.get_item_by_unique_id('some_random_item')

    def _encryption_key_that_raises_invalid_password_exception(self):
        encryption_key = getMock(EncryptionKey)
        encryption_key.provides("decrypt").raises(InvalidPasswordException)
        return encryption_key

    def _encryption_key_that_provides_decrypt(self):
        encryption_key = getMock(EncryptionKey)
        encryption_key.provides("decrypt")
        return encryption_key

    def _encryption_key_repository_that_returns_key(self, key):
        key_repository = getMock(EncryptionKeyRepository)
        key_repository.provides("key_for_security_level").with_args("SL5").returns(key)
        return key_repository
