from openpassword._keychain import Keychain


class AgileKeychain(Keychain):
    def __init__(self, path):
        super(AgileKeychain, self).__init__()
        self.initialised = False
