from unittest.mock import patch, MagicMock, call
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

        key3.decrypt_with_password.assert_called_with('password')
        key5.decrypt_with_password.assert_called_with('password')

        assert data_source.is_authenticated() is True

    @patch("openpassword.agile_keychain._key.Key")
    @patch("openpassword.agile_keychain._key.Key")
    @patch("openpassword.agile_keychain._key_manager.KeyManager")
    @raises(IncorrectPasswordException)
    def it_fails_authentication_if_a_key_can_not_be_validated(self, key_manager, key3, key5):
        key_manager.return_value.get_keys.return_value = [key3, key5]
        key3.decrypt_with_password.side_effect = KeyValidationException

        data_source = DataSource('some_path', key_manager=key_manager)
        data_source.authenticate('password')

        assert data_source.is_authenticated() is False

    @patch("openpassword.agile_keychain._key.Key")
    @patch("openpassword.agile_keychain._key.Key")
    @patch("openpassword.agile_keychain._key_manager.KeyManager")
    def it_re_encrypts_theys_with_new_password_when_password_is_changed(self, key_manager, key3, key5):
        key_manager_constructor = MagicMock(return_value=key_manager)
        key_manager.get_keys.return_value = [key3, key5]

        data_source = DataSource('some_path', key_manager=key_manager_constructor)
        data_source.authenticate('old_password')
        data_source.set_password('new_password')

        key3.decrypt_with_password.assert_called_with('old_password')
        key5.decrypt_with_password.assert_called_with('old_password')

        key3.encrypt_with_password.assert_called_with('new_password')
        key5.encrypt_with_password.assert_called_with('new_password')

        key_manager.save_key.assert_has_calls([call(key3), call(key5)])
