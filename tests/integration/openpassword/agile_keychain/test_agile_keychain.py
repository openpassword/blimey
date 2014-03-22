import os
from nose.tools import *
from openpassword import AgileKeychain
from subprocess import call


class AgileKeychainTest:
    def it_creates_agile_keychain_folder_structure_on_initialise(self):
        temporary_path = "somefolder"
        agile_keychain = AgileKeychain(temporary_path)
        agile_keychain.initialise("somepassword")

        assert os.path.exists(temporary_path) and os.path.isdir(temporary_path)

        data_default_dir = os.path.join(temporary_path, "data", "default")
        assert os.path.exists(data_default_dir) and os.path.isdir(data_default_dir)

        keys_file = os.path.join(data_default_dir, '1password.keys')
        assert os.path.exists(keys_file) and os.path.isfile(keys_file)

        contents_file = os.path.join(data_default_dir, 'contents.js')
        assert os.path.exists(contents_file) and os.path.isfile(contents_file)

        encryption_keys_file = os.path.join(data_default_dir, 'encryptionKeys.js')
        assert os.path.exists(encryption_keys_file) and os.path.isfile(encryption_keys_file)

        call(['rm', '-fr', temporary_path])

    def it_is_created_initialised_with_path_to_existing_keychain(self):
        agile_keychain = AgileKeychain(os.path.join('tests', 'fixtures', 'test.agilekeychain'))
        eq_(agile_keychain.is_initialised(), True)

    def it_is_created_non_initialised_with_path_to_non_existing_keychain(self):
        agile_keychain = AgileKeychain("nonexistingfolder")
        eq_(agile_keychain.is_initialised(), False)
