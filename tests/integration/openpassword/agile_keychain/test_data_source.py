import os
import sys
from nose.tools import eq_
import shutil
from openpassword.agile_keychain import DataSource
import plistlib
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import b64decode


class AgileKeychainDataSourceTest:
    _temporary_path = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
    _password = "somepassword"

    def it_creates_agile_keychain_folder_structure_on_initialisation(self):
        self._initialise_data_source()
        self._check_keychain_dir()
        self._check_data_default_dir()
        self._check_keys_file()
        self._check_contents_file()
        self._check_encryption_keys_file()

    def it_stores_password_on_initialisation(self):
        self._initialise_data_source()

        encryption_keys_file = open(os.path.join(self._get_data_default_dir(), 'encryptionKeys.js'), "r")

        assert self._password in encryption_keys_file.read()
        encryption_keys_file.close()

    def it_verifies_password(self):
        self._initialise_data_source()
        assert self._data_source.verify_password(self._password)

    def it_sets_password(self):
        self._initialise_data_source()
        self._data_source.set_password("newpassword")

        encryption_keys_file = open(os.path.join(self._get_data_default_dir(), 'encryptionKeys.js'), "r")

        assert "newpassword" in encryption_keys_file.read()
        encryption_keys_file.close()

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

    def it_creates_encryption_and_validation_keys_on_initialisation(self):
        self._initialise_data_source()

        data_default_dir = os.path.join(self._temporary_path, "data", "default")
        keys_file = os.path.join(data_default_dir, '1password.keys')
        keys = self._read_keys_from_keys_plist_file(keys_file)

        self._verify_keys_for_security_level(keys, 'SL5', self._password)
        self._verify_keys_for_security_level(keys, 'SL3', self._password)

    def _initialise_data_source(self):
        self._data_source = DataSource(self._temporary_path)
        self._data_source.initialise(self._password)
        self.teardown = self._path_clean

    def _path_clean(self):
        shutil.rmtree(self._temporary_path)

    def _get_data_default_dir(self):
        return os.path.join(self._temporary_path, "data", "default")

    def _check_keychain_dir(self):
        assert self._exists_and_is_dir(self._temporary_path)

    def _check_data_default_dir(self):
        assert self._exists_and_is_dir(self._get_data_default_dir())

    def _check_keys_file(self):
        keys_file = os.path.join(self._get_data_default_dir(), '1password.keys')
        assert self._exists_and_is_file(keys_file)

    def _check_contents_file(self):
        contents_file = os.path.join(self._get_data_default_dir(), 'contents.js')
        assert self._exists_and_is_file(contents_file)

    def _check_encryption_keys_file(self):
        encryption_keys_file = os.path.join(self._get_data_default_dir(), 'encryptionKeys.js')
        assert self._exists_and_is_file(encryption_keys_file)

    def _exists_and_is_file(self, path):
        return os.path.exists(path) and os.path.isfile(path)

    def _exists_and_is_dir(self, path):
        return os.path.exists(path) and os.path.isdir(path)

    def _read_keys_from_keys_plist_file(self, path):
        data = open(path, 'rb').read()
        data = self._remove_null_bytes(data)

        if sys.version_info < (3, 4, 0):
            keys = plistlib.readPlistFromBytes(data)
        else:
            keys = plistlib.loads(data)

        return keys

    def _verify_keys_for_security_level(self, keys, security_level, password):
        key_object = self._extract_key(keys, security_level)
        encryption_key = self._decrypt_encryption_key(key_object, password)
        validation_key = self._decrypt_validation_key(key_object, encryption_key)

        assert encryption_key
        assert validation_key
        assert validation_key == encryption_key

    def _remove_null_bytes(self, data):
        result = b''
        last = 0

        index = data.find(b'\x00')
        while index != -1:
            result = result + data[last:index]
            last = index + 1
            index = data.find(b'\x00', last)

        result = result + data[last:]

        return result

    def _extract_key(self, keys, security_level):
        for key in keys['list']:
            if key['level'] == security_level:
                key['data'] = b64decode(key['data'])
                key['validation'] = b64decode(key['validation'])
                return key

    def _decrypt_encryption_key(self, key_object, password):
        password_key = self._derive_key_from_password(key_object, password)
        return self._decrypt(key_object['data'][16:], password_key)

    def _derive_key_from_password(self, key_object, password):
        key = PBKDF2(password, key_object['data'][8:16], key_object['iterations'])
        return key.read(32)

    def _decrypt(self, data, key_iv):
        key = key_iv[0:16]
        iv = key_iv[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)

        return cipher.decrypt(data)

    def _decrypt_validation_key(self, key_object, encryption_key):
        validation_key = self._derive_validation_key(key_object, encryption_key)
        return self._decrypt(key_object['validation'][16:], validation_key)

    def _derive_validation_key(self, key_object, encryption_key):
        return self._derive_openssl_key(encryption_key, key_object['validation'][8:16])

    def _derive_openssl_key(self, key, salt):
        key = key[0:-16]
        openssl_key = bytes()
        prev = bytes()
        while len(openssl_key) < 32:
            prev = MD5.new(prev + key + salt).digest()
            openssl_key += prev

        return openssl_key
