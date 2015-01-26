import os
import shutil
from nose.tools import raises

from openpassword.agile_keychain._manager._file_system_manager import FileSystemManager

AGILE_KEYCHAIN_BASE_FILES = ['1password.keys', 'contents.js', 'encryptionKeys.js']


class FileSystemManagerTest:
    _temporary_path = os.path.join('tests', 'fixtures', 'temp.agilekeychain')

    def it_creates_agile_keychain_folder_structure_on_initialisation(self):
        self._initialise()
        self._check_keychain_dir()
        self._check_data_default_dir()
        self._check_config_dir()
        self._check_keys_file()
        self._check_contents_file()
        self._check_buildnum_file()
        self._check_encryption_keys_file()

    def it_is_created_initialised_with_path_to_existing_keychain(self):
        file_system_manager = FileSystemManager(os.path.join('tests', 'fixtures', 'test.agilekeychain'))
        assert file_system_manager.is_initialised() is True

    def it_is_created_non_initialised_with_path_to_non_existing_keychain(self):
        file_system_manager = FileSystemManager("nonexistingfolder")
        assert file_system_manager.is_initialised() is False

    def _initialise(self):
        self._file_system_manager = FileSystemManager(self._temporary_path)
        self._file_system_manager.initialise()
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
