from collections import defaultdict

from openpassword import abstract


class EncryptedItem(defaultdict):
    def __init__(self, data):
        self.update(data)

    def __missing__(self, key):
        return None


class DecryptedItem(defaultdict):
    def __init__(self, data):
        self.update(data)

    def __missing__(self, key):
        return None

    @staticmethod
    def create():
        return DecryptedItem({
            'uuid': '123123'
        })
