import os
import json
from openpassword import abstract

AGILE_KEYCHAIN_BASE_FILES = ['1password.keys', 'contents.js', 'encryptionKeys.js']


class DataSource(abstract.DataSource):
    def __init__(self, path):
        self.base_path = path
        self._default_folder = os.path.join(self.base_path, "data", "default")

    def initialise(self, password):
        os.makedirs(self._default_folder)

        for agile_keychain_base_file in AGILE_KEYCHAIN_BASE_FILES:
            open(os.path.join(self._default_folder, agile_keychain_base_file), "w+").close()

        self.set_password(password)

    def is_keychain_initialised(self):
        return self._validate_agile_keychain_base_files() and self._is_valid_folder(self._default_folder)

    def add_item(self, item):
        file_handle = open(os.path.join(self._default_folder, "{0}.1password".format(item['id'])), "w")
        json.dump(item, file_handle)
        file_handle.close()

    def verify_password(self, password):
        file_handle = open(os.path.join(self._default_folder, "encryptionKeys.js"), "r")
        password_found = False

        if password in file_handle.read():
            password_found = True

        file_handle.close()
        return password_found

    def set_password(self, password):
        file_handle = open(os.path.join(self._default_folder, "encryptionKeys.js"), "w")
        file_handle.write(password)
        file_handle.close()

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
