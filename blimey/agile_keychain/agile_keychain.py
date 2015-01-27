from blimey._keychain import Keychain
from blimey.agile_keychain import DataSource


class AgileKeychain(Keychain):
    def __init__(self, path):
        super(AgileKeychain, self).__init__(DataSource(path))
