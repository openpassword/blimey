import fudge
from nose.tools import *

from openpassword._keychain import Keychain
from openpassword.abstract import DataSource
from openpassword.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException
from spec.openpassword.fudge_wrapper import getMock


class KeychainSpec:
    def it_is_created_locked(self):
        keychain = self._get_simple_keychain()
        eq_(keychain.is_locked(), True)

    def it_unlocks_the_keychain_with_the_right_password(self):
        keychain = self._get_simple_keychain()
        keychain.unlock('rightpassword')
        eq_(keychain.is_locked(), False)

    def it_is_iterable_as_list_of_items_when_unlocked(self):
        keychain = self._get_simple_keychain()
        keychain.unlock("righpassowrd")

        try:
            iter(keychain)
        except TypeError:
            raise AssertionError("Keychain is not iterable")

    def it_locks_the_keychain(self):
        keychain = self._get_simple_keychain()
        keychain.unlock('rightpassword')
        eq_(keychain.is_locked(), False)

        keychain.lock()
        eq_(keychain.is_locked(), True)

    @raises(NonInitialisedKeychainException)
    def it_raises_NonInitialisedKeychainException_when_unlocking_uninitialized_keychain(self):
        keychain = self._get_non_initialised_keychain()
        keychain.unlock("somepassword")

    def it_is_initialisable_using_a_password(self):
        keychain = self._get_non_initialised_keychain()
        keychain.initialise("somepassword")
        eq_(keychain.is_initialised(), True)

    def it_keeps_uninitialised_if_we_dont_initialise_it(self):
        keychain = self._get_non_initialised_keychain()
        eq_(keychain.is_initialised(), False)

    def it_delegates_initialisation_to_the_data_source(self):
        fudge.clear_expectations()

        data_source = getMock(DataSource)
        data_source.provides("keychain_is_already_initialised")
        data_source.expects("initialise")

        keychain = Keychain(data_source)
        keychain.initialise("somepassword")

        fudge.verify()

    def it_is_created_initialised_for_an_initialised_data_source(self):
        fudge.clear_expectations()

        data_source = getMock(DataSource)
        data_source.provides("keychain_is_already_initialised").returns(True)

        keychain = Keychain(data_source)
        eq_(keychain.is_initialised(), True)

    def it_is_created_non_initialised_for_a_non_initialised_data_source(self):
        fudge.clear_expectations()

        data_source = getMock(DataSource)
        data_source.provides("keychain_is_already_initialised").returns(False)

        keychain = Keychain(data_source)
        eq_(keychain.is_initialised(), False)

    @raises(KeychainAlreadyInitialisedException)
    def it_throws_KeychainAlreadyInitialisedException_if_I_initialise_an_already_initialised_keychain(self):
        keychain = self._get_simple_keychain()
        keychain.initialise("somepassword")

    def _get_non_initialised_keychain(self):
        keychain = self._get_simple_keychain()
        keychain.initialised = False
        return keychain

    def _get_simple_keychain(self):
        data_source = getMock(DataSource)
        data_source.provides("initialise")
        data_source.provides("keychain_is_already_initialised").returns(True)
        return Keychain(data_source)
