class NonInitialisedKeychainException(Exception):
    pass


class KeychainAlreadyInitialisedException(Exception):
    pass


class MissingIdAttributeException(Exception):
    pass


class IncorrectPasswordException(Exception):
    pass


class KeychainLockedException(Exception):
    pass


class KeyValidationException(Exception):
    pass


class KeyAlreadyExistsForLevelException(Exception):
    pass


class InvalidKeyFileException(Exception):
    pass


class UnauthenticatedDataSourceException(Exception):
    pass
