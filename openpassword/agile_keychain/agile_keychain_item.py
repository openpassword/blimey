from openpassword.agile_keychain._key import Crypto


class AgileKeychainItem:
    def __init__(self):
        self.id = Crypto.generate_id()
        self.secrets = {}
