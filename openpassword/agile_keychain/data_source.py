import os
from openpassword import abstract

KEYCHAIN_BASE_FILES = ['1password.keys', 'contents.js', 'encryptionKeys.js']


class DataSource(abstract.DataSource):
    def __init__(self, path):
        self.base_path = path
        self._default_folder = os.path.join(self.base_path, "data", "default")

    def initialise(self):
        os.makedirs(self._default_folder)

        for f in KEYCHAIN_BASE_FILES:
            open(os.path.join(self._default_folder, f), "w+").close()

    def is_keychain_initialised(self):
        is_initialised = True
        for f in KEYCHAIN_BASE_FILES:
            current_file = os.path.join(self._default_folder, f)
            is_initialised = is_initialised and (os.path.exists(current_file) and os.path.isfile(current_file))

        return is_initialised and (os.path.exists(self._default_folder) and os.path.isdir(self._default_folder))
