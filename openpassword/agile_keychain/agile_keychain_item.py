from collections import defaultdict

from openpassword import abstract


class EncryptedAgileKeychainItem(defaultdict):
    def __init__(self, data):
        self.update(data)

    def __missing__(self, key):
        return None


class AgileKeychainItem(defaultdict):
    def __init__(self, data):
        self.update(data)

    def __missing__(self, key):
        return None
