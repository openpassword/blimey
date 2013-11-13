from nose.tools import *
from openpassword import EncryptionKey
from openpassword import Keychain
from openpassword.exceptions import InvalidPasswordException

import fudge
import time


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

    def it_triggers_a_callback_when_lock_timesout(self):
        EncryptionKey = fudge.Fake('encryption_key')
        EncryptionKey.provides("decrypt")

        spy = Spy()

        keychain = Keychain(EncryptionKey, 0.0005, spy.callback)
        keychain.unlock('rightpassword')
        time.sleep(0.005)
        eq_(spy.called, True)

    def it_locks_after_a_timeout_period(self):
        EncryptionKey = fudge.Fake('encryption_key')
        EncryptionKey.provides("decrypt")

        keychain = Keychain(EncryptionKey, 0.05)
        keychain.unlock('rightpassword')
        eq_(keychain.is_locked(), False)

        time.sleep(0.5)

        eq_(keychain.is_locked(), True)

class Spy:
    def __init__(self):
        self.called = False

    def callback(self):
        self.called = True
