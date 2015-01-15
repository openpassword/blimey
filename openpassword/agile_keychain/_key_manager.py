import os
import plistlib
from jinja2 import Template
from base64 import b64encode, b64decode

from openpassword.agile_keychain._key import Key
from openpassword.exceptions import KeyAlreadyExistsForLevelException

DEFAULT_ITERATIONS = 25000


class KeyManager:
    def __init__(self, path):
        self._base_path = path

    def get_keys(self):
        return self._read_keys_from_keys_plist()

    def create_key(self, password, security_level='SL5', iterations=DEFAULT_ITERATIONS):
        return Key.create(password, security_level, iterations)

    def save_key(self, new_key):
        existing_keys = self._read_keys_from_keys_plist()

        keys = []
        for old_key in existing_keys:
            if old_key.security_level == new_key.security_level:
                raise KeyAlreadyExistsForLevelException()

            if old_key.identifier != new_key.identifier:
                keys.append(old_key)

        keys.append(new_key)
        keys = [self._serialize_key(key) for key in keys]

        template_path = os.path.join(os.path.dirname(__file__), '1password.keys.template')

        with open(template_path, 'r') as file:
            plist_template = Template(file.read())

        with open(os.path.join(self._base_path, 'data', 'default', '1password.keys'), 'w') as file:
            file.write(plist_template.render({'keys': keys}))

    def _serialize_key(self, key):
        return {
            'identifier': key.identifier,
            'iterations': key.iterations,
            'data': (b64encode(key.data) + b'\x00').decode('ascii'),
            'validation': (b64encode(key.validation) + b'\x00').decode('ascii'),
            'level': key.security_level
        }

    def _read_keys_from_keys_plist(self):
        if os.path.exists(os.path.join(self._base_path, 'data', 'default', '1password.keys')):
            with open(os.path.join(self._base_path, 'data', 'default', '1password.keys'), 'rb') as file:
                data = file.read()
                data = self._remove_null_bytes(data)
        else:
            return []

        try:
            keys = plistlib.loads(data)
        except plistlib.InvalidFileException:
            return []

        key_list = []

        for key in keys['list']:
            key_list.append(Key(key))

        return key_list

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
