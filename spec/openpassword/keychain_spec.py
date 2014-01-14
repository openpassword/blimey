from nose.tools import *
from openpassword import Keychain
from openpassword.exceptions import InvalidPasswordException

import fudge


class KeychainSpec:

    def it_unlocks_the_keychain_with_the_right_password(self):
        key = fudge.Fake('encryption_key')
        key.provides("decrypt")

        key_repository = fudge.Fake('encryption_key_repository')
        key_repository.provides("key_for_security_level").with_args("SL5").returns(key)

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
        key = fudge.Fake('encryption_key')
        key.provides("decrypt")

        key_repository = fudge.Fake('encryption_key_repository')
        key_repository.provides("key_for_security_level").with_args("SL5").returns(key)

        item_repository = fudge.Fake('keychain_item_repository')

        keychain = Keychain(key_repository, item_repository)

        keychain.unlock('rightpassword')
        eq_(keychain.is_locked(), False)
        keychain.lock()
        eq_(keychain.is_locked(), True)
