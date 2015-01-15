import os
import sys
from nose.tools import eq_
import shutil
from openpassword.agile_keychain._key_manager import KeyManager
import plistlib
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import b64decode
from nose.tools import raises

from openpassword.exceptions import KeyAlreadyExistsForLevelException
from openpassword.agile_keychain._key import Key

if sys.version_info < (3, 4, 0):
    plistlib.loads = plistlib.readPlistFromBytes


class KeyManagerTest:
    _fixture_path = os.path.join('tests', 'fixtures', 'test.agilekeychain')
    _temporary_path = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
    _password = "somepassword"

    def it_loads_keys(self):
        key_manager = KeyManager(self._fixture_path)
        level3_key, level5_key = key_manager.get_keys()

        level3_key.validate('masterpassword123')
        assert level3_key.identifier == 'BE4CC37CD7C044E79B5CC1CC19A82A13'
        assert level3_key.security_level == 'SL3'
        assert level3_key.iterations == 25000

        level5_key.validate('masterpassword123')
        assert level5_key.identifier == '98EB2E946008403280A3A8D9261018A4'
        assert level5_key.security_level == 'SL5'
        assert level5_key.iterations == 25000

    def it_adds_a_key(self):
        self._init_temporary_path()

        key_manager = KeyManager(self._temporary_path)

        key = Key.create(self._password, 'SL3', 10)
        key_manager.save_key(key)

        keys = key_manager.get_keys()
        assert keys[0].identifier == key.identifier

    def it_treats_key_identifiers_as_unique(self):
        self._init_temporary_path()

        key_manager = KeyManager(self._temporary_path)

        key1 = Key.create(self._password, 'SL3', 10)
        key_manager.save_key(key1)

        key2 = Key.create(self._password, 'SL5', 10)
        key2.identifier = key1.identifier
        key_manager.save_key(key2)

        keys = key_manager.get_keys()
        assert len(keys) == 1

    @raises(KeyAlreadyExistsForLevelException)
    def it_throws_a_keyalreadyexistsforlevelexception_when_saving_second_key_with_same_security_level(self):
        self._init_temporary_path()

        key_manager = KeyManager(self._temporary_path)

        key1 = Key.create(self._password, 'SL3', 10)
        key_manager.save_key(key1)

        key2 = Key.create(self._password, 'SL3', 10)
        key_manager.save_key(key2)

    def _init_temporary_path(self):
        os.makedirs(os.path.join(self._temporary_path, 'data', 'default'))
        self.teardown = self._path_clean

    def _path_clean(self):
        print('removing')
        print(self._temporary_path)
        shutil.rmtree(self._temporary_path)
