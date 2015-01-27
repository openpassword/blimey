import os


class FileSystemManager:
    AGILE_KEYCHAIN_BASE_FILES = ['1password.keys', 'contents.js', 'encryptionKeys.js']
    BUILD_NUMBER_FILE = 'buildnum'
    BUILD_NUMBER = '32009'

    def __init__(self, path):
        self._base_path = path
        self._default_folder = os.path.join(self._base_path, "data", "default")
        self._config_folder = os.path.join(self._base_path, "config")

    def initialise(self):
        os.makedirs(self._default_folder)
        os.makedirs(self._config_folder)
        self._create_buildnum_file()

        for agile_keychain_base_file in self.AGILE_KEYCHAIN_BASE_FILES:
            open(os.path.join(self._default_folder, agile_keychain_base_file), "w+").close()

    def is_initialised(self):
        return self._validate_agile_keychain_base_files() and self._is_valid_folder(self._default_folder)

    def _create_buildnum_file(self):
        buildnum_file = os.path.join(self._config_folder, self.BUILD_NUMBER_FILE)
        buildnum_file = open(buildnum_file, "w+")
        buildnum_file.write(self.BUILD_NUMBER)
        buildnum_file.close()

    def _validate_agile_keychain_base_files(self):
        is_initialised = True

        for base_file in self.AGILE_KEYCHAIN_BASE_FILES:
            current_file = os.path.join(self._default_folder, base_file)
            is_initialised = is_initialised and self._is_valid_file(current_file)

        return is_initialised

    def _is_valid_file(self, file):
        return os.path.exists(file) and os.path.isfile(file)

    def _is_valid_folder(self, folder):
        return os.path.exists(folder) and os.path.isdir(folder)
