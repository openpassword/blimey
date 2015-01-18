from unittest.mock import patch
from nose.tools import eq_, raises

from openpassword._keychain import Keychain
from openpassword.abstract import DataSource
from openpassword.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException, \
    MissingIdAttributeException, IncorrectPasswordException, KeychainLockedException, \
    UnauthenticatedDataSourceException


class KeychainSpec:
    @patch('openpassword.agile_keychain.data_source')
    def it_is_locked_if_the_data_source_has_not_been_authenticated(self, data_source):
        data_source.is_authenticated.return_value = False
        keychain = Keychain(data_source)
        keychain.initialise("somepassword")

        assert keychain.is_locked() == True

    @patch('openpassword.agile_keychain.data_source')
    def it_is_unlocked_if_the_data_source_has_been_authenticated(self, data_source):
        data_source.is_authenticated.return_value = True
        keychain = Keychain(data_source)
        keychain.initialise("somepassword")

        assert keychain.is_locked() == False

    @patch('openpassword.agile_keychain.data_source')
    def it_locks_itself_by_deauthenticating_the_data_source(self, data_source):
        keychain = Keychain(data_source)
        keychain.initialise("somepassword")
        keychain.lock()

        assert data_source.deauthenticate.called is True

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

    @raises(NonInitialisedKeychainException)
    def it_throws_noninitialisedkeychainexception_when_unlocking_uninitialized_keychain(self):
        keychain = self._get_non_initialised_keychain()
        keychain.unlock("somepassword")

    @patch("openpassword.abstract.DataSource")
    @raises(IncorrectPasswordException)
    def it_throws_incorrectpasswordexception_when_unlocking_with_incorrect_password(self, data_source):
        data_source.authenticate.side_effect = IncorrectPasswordException

        keychain = Keychain(data_source)
        keychain.unlock("wrongpassword")

    def it_is_initialisable_using_a_password(self):
        keychain = self._get_non_initialised_keychain()
        keychain.initialise("somepassword")
        eq_(keychain.is_initialised(), True)

    @patch('openpassword.agile_keychain.data_source')
    def it_passes_initialisation_configuraton_to_data_source(self, data_source):
        password = "somepassword"
        config = {"iterations": 10}
        keychain = Keychain(data_source)
        keychain.initialise(password, config)

        data_source.initialise.assert_called_with(password, config)

    def it_keeps_uninitialised_if_we_dont_initialise_it(self):
        keychain = self._get_non_initialised_keychain()
        eq_(keychain.is_initialised(), False)

    @patch('openpassword.agile_keychain.data_source')
    def it_delegates_initialisation_to_the_data_source(self, data_source):
        keychain = Keychain(data_source)
        keychain.initialise("somepassword")

        assert data_source.initialise.called is True

    @patch("openpassword.abstract.DataSource")
    @raises(KeychainLockedException)
    def it_throws_keychainlockedexception_if_adding_items_to_a_locked_keychain(self, data_source):
        data_source.add_item.side_effect = UnauthenticatedDataSourceException

        keychain = Keychain(data_source)
        keychain.append({"id": "someitem_id"})

    @patch('openpassword.agile_keychain.data_source')
    def it_delegates_item_creation_to_the_data_source(self, data_source):
        keychain = Keychain(data_source)
        keychain.append({"id": "someitem_id"})

        assert data_source.add_item.called is True

    def it_is_created_initialised_for_an_initialised_data_source(self):
        keychain = self._get_simple_keychain()
        eq_(keychain.is_initialised(), True)

    @patch('openpassword.agile_keychain.data_source')
    def it_is_created_non_initialised_for_a_non_initialised_data_source(self, data_source):
        data_source.is_keychain_initialised.return_value = False

        keychain = Keychain(data_source)
        eq_(keychain.is_initialised(), False)

    @raises(KeychainAlreadyInitialisedException)
    def it_throws_keychainalreadyinitialisedexception_if_initialising_existing_keychain(self):
        keychain = self._get_simple_keychain()
        keychain.initialise("somepassword")

    def it_adds_the_item_to_the_keychain_with_the_item_id_as_key(self):
        keychain = self._get_simple_keychain()
        item = {'id': 'new_item_id'}
        keychain.append(item)
        eq_(keychain['new_item_id'], item)

    def it_allows_for_items_to_be_appended(self):
        keychain = self._get_simple_keychain()
        new_item = {"id": "new_item"}
        keychain.append(new_item)
        eq_(new_item in keychain, True)

    def it_iterates_over_items(self):
        keychain = self._get_simple_keychain()
        items = [
            {'id': '123'},
            {'id': '456'},
            {'id': '789'}
        ]

        for item in items:
            keychain.append(item)

        for item in keychain:
            assert item in items

    @raises(MissingIdAttributeException)
    def it_throws_an_missingidattributeexception_when_id_attribute_is_missing_from_item(self):
        keychain = self._get_simple_keychain()
        new_item = {}
        keychain.append(new_item)

    @raises(KeychainLockedException)
    def it_throws_a_keychainlockedexception_when_setting_password_on_a_locked_keychain(self):
        keychain = self._get_simple_keychain()
        keychain.set_password("foobar")

    @patch("openpassword.abstract.DataSource")
    def it_changes_password(self, data_source_class):
        data_source = data_source_class.return_value
        data_source.authenticate.return_value = None
        data_source.set_password.return_value = None

        keychain = Keychain(data_source)
        keychain.unlock("password")
        keychain.set_password("foobar")

        data_source.set_password.assert_called_with("foobar")

    def _get_non_initialised_keychain(self):
        keychain = self._get_simple_keychain()
        keychain.initialised = False
        return keychain

    @patch.object(DataSource, 'is_keychain_initialised')
    def _get_simple_keychain(self, data_source):
        data_source.is_keychain_initialised.return_value = True

        return Keychain(data_source)
