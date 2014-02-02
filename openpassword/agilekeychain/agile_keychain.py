from openpassword import Keychain
from openpassword.agilekeychain.encryption_key_repository import EncryptionKeyRepository
from openpassword.agilekeychain.keychain_item_repository import KeychainItemRepository


class AgileKeychain(Keychain):
    def __init__(self, path):
        key_repository = EncryptionKeyRepository(path)
        item_repository = KeychainItemRepository(path)
        super(AgileKeychain, self).__init__(key_repository, item_repository)
