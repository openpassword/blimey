from collections import defaultdict

from openpassword import abstract


class EncryptedAgileKeychainItem(defaultdict):
    def __init__(self, data):
        self.update(data)

    def __missing__(self, key):
        return None

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, repr(dict(self)))


class AgileKeychainItem(defaultdict):
    def __init__(self, data):
        self.update(data)

    def __missing__(self, key):
        return None

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, repr(dict(self)))
