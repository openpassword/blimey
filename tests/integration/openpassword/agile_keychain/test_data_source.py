import os
import shutil
from nose.tools import raises

from openpassword.agile_keychain import DataSource
from openpassword.agile_keychain.agile_keychain_item import AgileKeychainItem
from openpassword.exceptions import IncorrectPasswordException, UnauthenticatedDataSourceException


class AgileKeychainDataSourceTest:
    _temporary_path = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
    _password = "somepassword"
    _data_source = None

    def it_creates_agile_keychain_folder_structure_on_initialisation(self):
        self._initialise_data_source()
        self._check_keychain_dir()
        self._check_data_default_dir()
        self._check_config_dir()
        self._check_keys_file()
        self._check_contents_file()
        self._check_buildnum_file()
        self._check_encryption_keys_file()

    def it_authenticates_with_a_password(self):
        self._initialise_data_source()
        self._data_source.authenticate(self._password)

    # We need a way to ensure garbage collection was also triggered
    def it_clears_keys_from_memory_when_deauthenticated(self):
        self._initialise_data_source()

        self._data_source.authenticate(self._password)
        assert len(self._data_source._keys) == 2

        self._data_source.deauthenticate()
        assert len(self._data_source._keys) == 0

    @raises(IncorrectPasswordException)
    def it_fails_authentication_with_incorrect_password_exception(self):
        self._initialise_data_source()
        self._data_source.authenticate('wrongpassord')

    def it_is_created_initialised_with_path_to_existing_keychain(self):
        data_source = DataSource(os.path.join('tests', 'fixtures', 'test.agilekeychain'))
        assert data_source.is_initialised()

    def it_is_created_non_initialised_with_path_to_non_existing_keychain(self):
        data_source = DataSource("nonexistingfolder")
        assert data_source.is_initialised() is False

    def it_reads_iteration_count_from_initialisation_configuration(self):
        iterations = 123

        data_source = DataSource(self._temporary_path)
        data_source.initialise(self._password, {'iterations': iterations})

        for key in data_source._key_manager.get_keys():
            assert key.iterations == iterations

        self.teardown = self._path_clean

    def it_retrieves_an_item_by_id(self):
        test_path = os.path.join('tests', 'fixtures', 'test.agilekeychain')
        data_source = DataSource(test_path)
        data_source.authenticate('masterpassword123')

        item = data_source.get_item_by_id('5F7210FD2F3F460692B7083C60854A02')

        assert item.secrets['path'] == '/some/path'
        assert item.secrets['username'] == 'someuser'
        assert item.secrets['password'] == 'password123'
        assert item.secrets['server'] == 'ftp://someserver.com'

        item = data_source.get_item_by_id('2E21D652E0754BD59F6B94B0323D0142')

        assert item.secrets['product_version'] == '1.2.3'
        assert item.secrets['reg_email'] == 'some.user@emailprovider.tld'
        assert item.secrets['reg_code'] == 'abc-license-123'
        assert item.secrets['reg_name'] == 'Some User'

    def it_retrieves_all_items(self):
        test_path = os.path.join('tests', 'fixtures', 'test.agilekeychain')
        data_source = DataSource(test_path)
        data_source.authenticate('masterpassword123')

        expected_item_ids = [
            '2E21D652E0754BD59F6B94B0323D0142',
            '4A3D784D115F4279BDFCE46D0A162D57',
            '5F7210FD2F3F460692B7083C60854A02',
            '6371E49FEFA042EDB335421459E5B29F',
            '9315F5EA8DCC4CB7BE09155DB7FCD1ED',
            '97019BEBCF9E402F8F0C033474B1B85D',
            '9E7673CCBB5B4AC9A7A8838835CB7E83',
            'B851D6E3232842B0858BC10968632A9C',
            'D05009E62D7D401CB8ACF2FE6981C031'
        ]

        for item in data_source.get_all_items():
            assert item.get_id() in expected_item_ids

    @raises(UnauthenticatedDataSourceException)
    def it_throws_if_adding_items_without_authenticating_first(self):
        self._initialise_data_source()
        self._data_source.add_item(AgileKeychainItem())

    def it_adds_an_item_to_the_keychain(self):
        self._initialise_data_source()
        self._data_source.authenticate(self._password)

        item = AgileKeychainItem()
        item.secrets['username'] = 'mulder'
        item.secrets['password'] = 'trustno1'

        self._data_source.add_item(item)

        retrieved_item = self._data_source.get_item_by_id(item.get_id())

        assert item.secrets['username'] == retrieved_item.secrets['username']
        assert item.secrets['password'] == retrieved_item.secrets['password']

    def _initialise_data_source(self):
        self._data_source = DataSource(self._temporary_path)
        self._data_source.initialise(self._password, {'iterations': 10})
        self.teardown = self._path_clean

    def _path_clean(self):
        shutil.rmtree(self._temporary_path)

    def _get_data_default_dir(self):
        return os.path.join(self._temporary_path, "data", "default")

    def _get_config_dir(self):
        return os.path.join(self._temporary_path, 'config')

    def _check_keychain_dir(self):
        assert self._exists_and_is_dir(self._temporary_path)

    def _check_data_default_dir(self):
        assert self._exists_and_is_dir(self._get_data_default_dir())

    def _check_config_dir(self):
        assert self._exists_and_is_dir(self._get_config_dir())

    def _check_keys_file(self):
        keys_file = os.path.join(self._get_data_default_dir(), '1password.keys')
        assert self._exists_and_is_file(keys_file)

    def _check_contents_file(self):
        contents_file = os.path.join(self._get_data_default_dir(), 'contents.js')
        assert self._exists_and_is_file(contents_file)

    def _check_buildnum_file(self):
        buildnum_file = os.path.join(self._get_config_dir(), 'buildnum')
        assert self._exists_and_is_file(buildnum_file)

    def _check_encryption_keys_file(self):
        encryption_keys_file = os.path.join(self._get_data_default_dir(), 'encryptionKeys.js')
        assert self._exists_and_is_file(encryption_keys_file)

    def _exists_and_is_file(self, path):
        return os.path.exists(path) and os.path.isfile(path)

    def _exists_and_is_dir(self, path):
        return os.path.exists(path) and os.path.isdir(path)
