class EncryptionKeyFactory:
    def __init__(self, keys):
        self.keys = keys

    def key_for_security_level(self, security_level):
        identifier = self.keys[security_level]

        for key in self.keys["list"]:
            if key["identifier"] == identifier:
                return key
