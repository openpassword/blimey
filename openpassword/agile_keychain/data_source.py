import os
import json
import gc
import glob

from base64 import b64decode, b64encode
from openpassword.agile_keychain._key import Crypto
from math import fmod

from openpassword import abstract
from openpassword.exceptions import KeyValidationException, IncorrectPasswordException, \
    UnauthenticatedDataSourceException
from openpassword.agile_keychain._key_manager import KeyManager
from openpassword.agile_keychain.agile_keychain_item import AgileKeychainItem

AGILE_KEYCHAIN_BASE_FILES = ['1password.keys', 'contents.js', 'encryptionKeys.js']
DEFAULT_ITERATIONS = 25000


class DataSource(abstract.DataSource):
    BUILD_NUMBER_FILE = 'buildnum'
    BUILD_NUMBER = '32009'

    def __init__(self, path, key_manager=KeyManager):
        self._base_path = path
        self._default_folder = os.path.join(self._base_path, "data", "default")
        self._config_folder = os.path.join(self._base_path, "config")
        self._key_manager = key_manager(self._base_path)
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
                key.decrypt_with_password(password)
            except KeyValidationException:
                raise IncorrectPasswordException

            self._keys.append(key)

    def deauthenticate(self):
        self._keys = []
        gc.collect()

    def is_authenticated(self):
        if len(self._keys) == 0:
            return False

        for key in self._keys:
            if key.decrypted_key is None:
                return False

        return True

    def set_password(self, password):
        for key in self._keys:
            key.encrypt_with_password(password)
            self._key_manager.save_key(key)

    def add_item(self, item):
        if self.is_authenticated() is False:
            raise UnauthenticatedDataSourceException()

        key = self._get_default_key()
        init_vector = os.urandom(8)
        derived_key = Crypto.derive_key(key.decrypted_key, init_vector)

        data = json.dumps(item.secrets)
        data = byte_pad(data.encode('utf8'), 16)
        data = Crypto.encrypt(derived_key[0:16], derived_key[16:], data)

        encrypted_data = b'Salted__' + init_vector + data

        data = {
            'uuid': item.id,
            'encrypted': b64encode(byte_pad(encrypted_data)).decode('ascii'),
            'openContents': {}
        }

        with open(os.path.join(self._default_folder, "{0}.1password".format(item.id)), "w") as file:
            json.dump(data, file)

    def get_item_by_id(self, item_id):
        item_path = os.path.join(self._base_path, "data", "default", item_id + ".1password")
        with open(item_path, 'r') as file:
            data = json.load(file)

        key = self._get_key_for_item(data)

        encrypted = b64decode(data['encrypted'])
        init_vector = encrypted[8:16]
        derived_key = Crypto.derive_key(key.decrypted_key, init_vector)
        decrypted = Crypto.decrypt(derived_key[0:16], derived_key[16:], encrypted[16:])
        decrypted = strip_byte_padding(decrypted)
        decrypted_data = json.loads(decrypted.decode('ascii'))

        item = AgileKeychainItem()
        item.id = data['uuid']
        item.secrets = decrypted_data

        return item

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
        if 'securityLevel' in item['openContents']:
            return self._get_key_by_security_level(item['openContents']['securityLevel'])

        return self._get_default_key()

    def _get_key_by_security_level(self, security_level):
        return [key for key in self._keys if key.security_level == security_level][0]

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
        level3_key = self._key_manager.create_key(password, security_level='SL3', iterations=iterations)
        level5_key = self._key_manager.create_key(password, security_level='SL5', iterations=iterations)

        self._key_manager.save_key(level3_key)
        self._key_manager.save_key(level5_key)


def byte_pad(input_bytes, length=8):
    if length > 256:
        raise ValueError("Maximum padding length is 256")

    # Modulo input bytes length with padding length to see how many bytes to pad with
    bytes_to_pad = length - int(fmod(len(input_bytes), length))

    if bytes_to_pad == length:
        bytes_to_pad = 0

    # Pad input bytes with a sequence of bytes containing the number of padded bytes
    input_bytes += bytes([bytes_to_pad] * bytes_to_pad)

    return input_bytes


def strip_byte_padding(input_bytes, length=16):
    if fmod(len(input_bytes), length) != 0:
        raise ValueError("Input byte length is not divisible by %s " % length)

    # Get the last {length} bytes of the input bytes, reversed
    if len(input_bytes) == length:
        byte_block = bytes(input_bytes[::-1])
    else:
        byte_block = bytes(input_bytes[:length:-1])

    # If input bytes is padded, the padding is equal to byte value of the number
    # of bytes padded. So we can read the padding value from the last byte..
    padding_byte = byte_block[0:1]

    for i in range(1, ord(padding_byte.decode())):
        if byte_block[i:i+1] != padding_byte:
            return input_bytes

    return input_bytes[0:-ord(padding_byte.decode())]
