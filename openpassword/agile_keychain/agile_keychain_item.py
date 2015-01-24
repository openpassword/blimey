from collections import defaultdict


class EncryptedAgileKeychainItem(defaultdict):
    def __init__(self, data):
        super().__init__(None, data)

    def __missing__(self, key):
        return None

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, repr(dict(self)))


class AgileKeychainItem(defaultdict):
    def __init__(self, data):
        super().__init__(None, data)

    def __missing__(self, key):
        return None

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, repr(dict(self)))
