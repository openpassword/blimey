from openpassword.agile_keychain._key import Crypto
from openpassword import abstract


class AgileKeychainItem(abstract.Item):
    def __init__(self):
        self.id = Crypto.generate_id()
        self.secrets = {}

    def get_id(self):
        return self.id
