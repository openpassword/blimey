import json


class EncryptionKeyRepository:
    def __init__(self, path):
        self._path = path

    def key_for_security_level(self, security_level):
        key_file_path = self._resolve_key_file_path()
        keys = self._load_key_data(key_file_path)

        identifier = keys[security_level]

        for key in keys["list"]:
            if key["identifier"] == identifier:
                return key

    def _resolve_key_file_path(self):
        return self._path + '/data/default/encryptionKeys.js'

    def _load_key_data(self, path):
        try:
            file = open(path)
        except IOError:
            raise InvalidUuidException("Invalid path: %s" % path)

        data = json.load(file)
        file.close()

        return data
