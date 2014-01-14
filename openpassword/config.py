class Config:
    def __init__(self):
        self._keychain_path = None

    def set_path(self, path=None):
        self._keychain_path = path

    def get_path(self):
        return self._keychain_path
