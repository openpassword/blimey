from abc import ABCMeta, abstractmethod


class EncryptionKeyRepository(metaclass=ABCMeta):

    @abstractmethod
    def key_for_security_level(self, security_level):
        return NotImplemented
