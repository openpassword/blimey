from base64 import b64decode


class EncryptedKey():
    def __init__(self, key):
        self.identifier = key['identifier']
        self.level = key['level']
        self.iterations = key['iterations']
        self.data = b64decode(key['data'])
        self.validation = b64decode(key['validation'])


class DecryptedKey():
    def __init__(self, key):
        self.identifier = key['identifier']
        self.level = key['level']
        self.iterations = key['iterations']
        self.key = key['key']
