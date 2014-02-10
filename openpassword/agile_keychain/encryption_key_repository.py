import json
from openpassword.agile_keychain.encryption_key import EncryptionKey
from openpassword.exceptions import EncryptionKeyNotFoundException
from openpassword.exceptions import InvalidUuidException
from openpassword import abstract


class EncryptionKeyRepository(abstract.EncryptionKeyRepository):
    def __init__(self, path):
        self._path = path
        self._keys = None

    def key_for_security_level(self, security_level):
        self._load_keys()

        key_id = self._resolve_key_id_for_security_level(security_level)
        return self._get_key_by_id(key_id)

    def _load_keys(self):
        key_file_path = self._resolve_key_file_path()
        self.keys = self._load_key_data(key_file_path)

    def _resolve_key_file_path(self):
        return self._path + '/data/default/encryptionKeys.js'

    def _load_key_data(self, path):
        try:
            file = open(path)
        except IOError:
            raise InvalidUuidException("Invalid path: {0}".format(path))

        data = json.load(file)
        file.close()

        return data

    def _resolve_key_id_for_security_level(self, security_level):
        try:
            return self.keys[security_level]
        except KeyError:
            raise EncryptionKeyNotFoundException("Unknown security level: {0}".format(security_level))

    def _get_key_by_id(self, key_id):
        for key in self.keys["list"]:
            if key["identifier"] == key_id:
                return EncryptionKey(key)
