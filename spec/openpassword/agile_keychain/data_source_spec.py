from unittest.mock import patch
from nose.tools import raises

from openpassword.agile_keychain import DataSource
from openpassword.exceptions import KeyValidationException, IncorrectPasswordException


class DataSourceSpec:
    @patch("openpassword.agile_keychain._key_manager.KeyManager")
    def it_constructs_a_key_manager_with_the_same_path(self, key_manager):
        DataSource('some_path', key_manager=key_manager)
        key_manager.assert_called_with('some_path')

    @patch("openpassword.agile_keychain._key.Key")
    @patch("openpassword.agile_keychain._key.Key")
    @patch("openpassword.agile_keychain._key_manager.KeyManager")
    def it_authenticates_against_all_keys(self, key_manager, key3, key5):
        key_manager.return_value.get_keys.return_value = [key3, key5]

        data_source = DataSource('some_path', key_manager=key_manager)
        data_source.authenticate('password')

        key3.validate.assert_called_with('password')
        key5.validate.assert_called_with('password')

    @patch("openpassword.agile_keychain._key.Key")
    @patch("openpassword.agile_keychain._key.Key")
    @patch("openpassword.agile_keychain._key_manager.KeyManager")
    @raises(IncorrectPasswordException)
    def it_fails_authentication_if_a_key_can_not_be_validated(self, key_manager, key3, key5):
        key_manager.return_value.get_keys.return_value = [key3, key5]
        key3.validate.side_effect = KeyValidationException

        data_source = DataSource('some_path', key_manager=key_manager)
        data_source.authenticate('password')
