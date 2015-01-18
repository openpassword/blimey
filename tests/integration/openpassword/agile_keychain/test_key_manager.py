import os
import shutil
from openpassword.agile_keychain._key_manager import KeyManager
from nose.tools import raises

from openpassword.exceptions import KeyAlreadyExistsForLevelException, InvalidKeyFileException
from openpassword.agile_keychain._key import Key


class KeyManagerTest:
    _fixture_path = os.path.join('tests', 'fixtures', 'test.agilekeychain')
    _temporary_path = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
    _password = "somepassword"

    def it_loads_keys(self):
        key_manager = KeyManager(self._fixture_path)
        level3_key, level5_key = key_manager.get_keys()

        level3_key.decrypt_with_password('masterpassword123')
        level5_key.decrypt_with_password('masterpassword123')

        # Asserting that the key manager correctly loads and populates keys from the 1Password 3
        # generated fixture keychain. The identifiers are arbitrary, but security levels 3 and 5
        # are what 1Password uses internally, and the 25000 iteration PBKDF2 run is what
        # 1Password used as the default at the time the fixture was created.
        self._assert_key_properties(level3_key, 'BE4CC37CD7C044E79B5CC1CC19A82A13', 'SL3', 25000)
        self._assert_key_properties(level5_key, '98EB2E946008403280A3A8D9261018A4', 'SL5', 25000)

    def it_adds_a_key(self):
        self._init_key_file_with('')

        key_manager = KeyManager(self._temporary_path)

        key = Key.create(self._password, 'SL3', 10)
        key_manager.save_key(key)

        keys = key_manager.get_keys()
        assert keys[0].identifier == key.identifier

    def it_treats_key_identifiers_as_unique(self):
        self._init_key_file_with('')

        key_manager = KeyManager(self._temporary_path)

        key1 = Key.create(self._password, 'SL3', 10)
        key_manager.save_key(key1)

        key2 = Key.create(self._password, 'SL5', 10)
        key2.identifier = key1.identifier
        key_manager.save_key(key2)

        keys = key_manager.get_keys()
        assert len(keys) == 1

    @raises(KeyAlreadyExistsForLevelException)
    def it_throws_if_different_keys_are_on_same_level(self):
        self._init_key_file_with('')

        key_manager = KeyManager(self._temporary_path)

        key1 = Key.create(self._password, 'SL3', 10)
        key_manager.save_key(key1)

        key2 = Key.create(self._password, 'SL3', 10)
        key_manager.save_key(key2)

    def it_replaces_existing_key_with_same_identifier_and_security_level(self):
        self._init_key_file_with('')

        key_manager = KeyManager(self._temporary_path)

        key1 = Key.create(self._password, 'SL3', 10)
        key_manager.save_key(key1)

        key2 = Key.create(self._password, 'SL3', 10)
        key2.identifier = key1.identifier
        key_manager.save_key(key2)

        keys = key_manager.get_keys()
        assert len(keys) == 1

    @raises(InvalidKeyFileException)
    def it_throws_if_key_file_can_not_be_parsed(self):
        self._init_key_file_with('<foobar>!')
        key_manager = KeyManager(self._temporary_path)
        key_manager.get_keys()

    def _assert_key_properties(self, key, identifier, security_level, iterations):
        assert key.identifier == identifier
        assert key.security_level == security_level
        assert key.iterations == iterations

    def _init_key_file_with(self, contents):
        os.makedirs(os.path.join(self._temporary_path, 'data', 'default'))
        self.teardown = self._path_clean

        with open(os.path.join(self._temporary_path, 'data', 'default', '1password.keys'), 'w') as file:
            file.write(contents)

    def _path_clean(self):
        shutil.rmtree(self._temporary_path)
