from abc import ABCMeta, abstractmethod


class DataSource(metaclass=ABCMeta):

    @abstractmethod
    def initialise(self, path):
        return NotImplemented

    @abstractmethod
    def is_keychain_initialised(self):
        return NotImplemented
