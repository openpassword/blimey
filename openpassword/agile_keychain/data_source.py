import os
import gc
import glob

from openpassword import abstract
from openpassword.exceptions import KeyValidationException, IncorrectPasswordException, \
    UnauthenticatedDataSourceException
from openpassword.agile_keychain._key_manager import KeyManager
from openpassword.agile_keychain._item_manager import ItemManager
from openpassword.agile_keychain._crypto import create_key, decrypt_key, encrypt_key, decrypt_item, encrypt_item

AGILE_KEYCHAIN_BASE_FILES = ['1password.keys', 'contents.js', 'encryptionKeys.js']
DEFAULT_ITERATIONS = 25000


class DataSource(abstract.DataSource):
    BUILD_NUMBER_FILE = 'buildnum'
    BUILD_NUMBER = '32009'

    def __init__(self, path, key_manager=KeyManager, item_manager=ItemManager):
        self._base_path = path
        self._default_folder = os.path.join(self._base_path, "data", "default")
        self._config_folder = os.path.join(self._base_path, "config")
        self._key_manager = key_manager(self._base_path)
        self._item_manager = item_manager(self._base_path)
        self._keys = []

    def initialise(self, password, config=None):
        os.makedirs(self._default_folder)
        os.makedirs(self._config_folder)

        for agile_keychain_base_file in AGILE_KEYCHAIN_BASE_FILES:
            open(os.path.join(self._default_folder, agile_keychain_base_file), "w+").close()

        self._initialise_key_files(password, self._read_iterations_from_config(config))
        self._create_buildnum_file()

        self.set_password(password)

    def is_initialised(self):
        return self._validate_agile_keychain_base_files() and self._is_valid_folder(self._default_folder)

    def authenticate(self, password):
        keys = self._key_manager.get_keys()

        for key in keys:
            try:
                decrypted_key = decrypt_key(key, password)
            except KeyValidationException:
                raise IncorrectPasswordException

            self._keys.append(decrypted_key)

    def deauthenticate(self):
        self._keys = []
        gc.collect()

    def is_authenticated(self):
        if len(self._keys) == 0:
            return False

        for key in self._keys:
            if key.key is None:
                return False

        return True

    def set_password(self, password):
        for key in self._keys:
            encrypted_key = encrypt_key(key, password)
            self._key_manager.save_key(encrypted_key)

    def add_item(self, decrypted_item):
        if self.is_authenticated() is False:
            raise UnauthenticatedDataSourceException()

        encrypted_item = encrypt_item(decrypted_item, self._get_default_key())
        self._item_manager.save_item(encrypted_item)

    def get_item_by_id(self, item_id):
        if self.is_authenticated() is False:
            raise UnauthenticatedDataSourceException()

        encrypted_item = self._item_manager.get_by_id(item_id)

        return decrypt_item(encrypted_item, self._get_key_for_item(encrypted_item))

    def get_all_items(self):
        item_paths = glob.glob(os.path.join(self._base_path, "data", "default", "*.1password"))

        items = []
        for item_path in item_paths:
            basename = os.path.basename(item_path)
            item_id, _ = os.path.splitext(basename)
            items.append(self.get_item_by_id(item_id))

        return items

    def _create_buildnum_file(self):
        buildnum_file = os.path.join(self._config_folder, self.BUILD_NUMBER_FILE)
        buildnum_file = open(buildnum_file, "w+")
        buildnum_file.write(self.BUILD_NUMBER)
        buildnum_file.close()

    def _get_key_for_item(self, item):
        if item['openContents'] is None:
            return self._get_default_key()

        if 'securityLevel' not in item['openContents']:
            return self._get_default_key()

        return self._get_key_by_security_level(item['openContents']['securityLevel'])

    def _get_key_by_security_level(self, security_level):
        return [key for key in self._keys if key.level == security_level][0]

    def _get_default_key(self):
        return self._get_key_by_security_level('SL5')

    def _read_iterations_from_config(self, config):
        if type(config) is not dict:
            return DEFAULT_ITERATIONS

        if 'iterations' in config:
            return config['iterations']

        return DEFAULT_ITERATIONS

    def _validate_agile_keychain_base_files(self):
        is_initialised = True
        for base_file in AGILE_KEYCHAIN_BASE_FILES:
            current_file = os.path.join(self._default_folder, base_file)
            is_initialised = is_initialised and self._is_valid_file(current_file)
        return is_initialised

    def _is_valid_file(self, file):
        return os.path.exists(file) and os.path.isfile(file)

    def _is_valid_folder(self, folder):
        return os.path.exists(folder) and os.path.isdir(folder)

    def _initialise_key_files(self, password, iterations):
        level3_key = self._key_manager.create_key(password, level='SL3', iterations=iterations)
        level5_key = self._key_manager.create_key(password, level='SL5', iterations=iterations)

        self._key_manager.save_key(level3_key)
        self._key_manager.save_key(level5_key)
