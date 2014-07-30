import os
from nose.tools import *
import shutil
from openpassword.agile_keychain import DataSource


class AgileKeychainDataSourceTest:
    _temporary_path = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
    _password = "somepassword"

    def it_creates_agile_keychain_folder_structure_on_initialisation(self):
        self._initialise_data_source()

        assert os.path.exists(self._temporary_path) and os.path.isdir(self._temporary_path)

        data_default_dir = os.path.join(self._temporary_path, "data", "default")
        assert os.path.exists(data_default_dir) and os.path.isdir(data_default_dir)

        keys_file = os.path.join(data_default_dir, '1password.keys')
        assert os.path.exists(keys_file) and os.path.isfile(keys_file)

        contents_file = os.path.join(data_default_dir, 'contents.js')
        assert os.path.exists(contents_file) and os.path.isfile(contents_file)

        encryption_keys_file = os.path.join(data_default_dir, 'encryptionKeys.js')
        assert os.path.exists(encryption_keys_file) and os.path.isfile(encryption_keys_file)

    def it_stores_password_on_initialisation(self):
        self._initialise_data_source()

        data_default_dir = os.path.join(self._temporary_path, "data", "default")
        encryption_keys_file = open(os.path.join(data_default_dir, 'encryptionKeys.js'), "r")

        assert self._password in encryption_keys_file.read()
        encryption_keys_file.close()

    def it_verifies_password(self):
        self._initialise_data_source()
        assert self._data_source.verify_password(self._password)

    def it_sets_password(self):
        self._initialise_data_source()
        self._data_source.set_password("newpassword")

        data_default_dir = os.path.join(self._temporary_path, "data", "default")
        encryption_keys_file = open(os.path.join(data_default_dir, 'encryptionKeys.js'), "r")

        assert "newpassword" in encryption_keys_file.read()
        encryption_keys_file.close()

    def _initialise_data_source(self):
        self._data_source = DataSource(self._temporary_path)
        self._data_source.initialise(self._password)
        self.teardown = self._path_clean

    def _path_clean(self):
        shutil.rmtree(self._temporary_path)

    def it_is_created_initialised_with_path_to_existing_keychain(self):
        data_source = DataSource(os.path.join('tests', 'fixtures', 'test.agilekeychain'))
        eq_(data_source.is_keychain_initialised(), True)

    def it_is_created_non_initialised_with_path_to_non_existing_keychain(self):
        data_source = DataSource("nonexistingfolder")
        eq_(data_source.is_keychain_initialised(), False)

    def it_adds_new_items_to_the_keychain(self):
        data_source = DataSource(os.path.join('tests', 'fixtures', 'test.agilekeychain'))
        data_source.add_item({'id': '79cd94b00ab34d209d62e487e77965a5'})

        assert os.path.exists(os.path.join('tests', 'fixtures', 'test.agilekeychain', 'data', 'default',
                                           '79cd94b00ab34d209d62e487e77965a5.1password')) is True
        os.remove(os.path.join('tests', 'fixtures', 'test.agilekeychain', 'data', 'default',
                               '79cd94b00ab34d209d62e487e77965a5.1password'))
