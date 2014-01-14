from nose.tools import *
from openpassword import Keychain
from openpassword.exceptions import InvalidPasswordException

import fudge


class KeychainSpec:

    def it_unlocks_the_keychain_with_the_right_password(self):
        EncryptionKey = fudge.Fake('encryption_key')
        EncryptionKey.provides("decrypt")

        keychain = Keychain(EncryptionKey)
        keychain.unlock('rightpassword')

        eq_(keychain.is_locked(), False)

    @raises(InvalidPasswordException)
    def it_raises_invalidpasswordexception_with_wrong_password(self):
        EncryptionKey = fudge.Fake('encryption_key')
        EncryptionKey.provides("decrypt").raises(InvalidPasswordException)

        keychain = Keychain(EncryptionKey)
        keychain.unlock('wrongpassword')

    def it_fails_to_unlock_with_wrong_password(self):
        EncryptionKey = fudge.Fake('encryption_key')
        EncryptionKey.provides("decrypt").raises(InvalidPasswordException)

        keychain = Keychain(EncryptionKey)
        try:
            keychain.unlock('wrongpassword')
        except:
            pass

        eq_(keychain.is_locked(), True)

    def it_locks_when_lock_is_called(self):
        EncryptionKey = fudge.Fake('encryption_key')
        EncryptionKey.provides("decrypt")

        keychain = Keychain(EncryptionKey)
        keychain.unlock('rightpassword')
        eq_(keychain.is_locked(), False)
        keychain.lock()
        eq_(keychain.is_locked(), True)
