from abc import ABCMeta, abstractmethod


class DataSource(metaclass=ABCMeta):

    @abstractmethod
    def initialise(self, path, config=None):
        return NotImplemented

    @abstractmethod
    def is_keychain_initialised(self):
        return NotImplemented

    @abstractmethod
    def add_item(self, item):
        return NotImplemented

    @abstractmethod
    def authenticate(self, password):
        return NotImplemented
