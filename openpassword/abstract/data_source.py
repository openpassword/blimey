from abc import ABCMeta, abstractmethod


class DataSource(metaclass=ABCMeta):

    @abstractmethod
    def initialise(self, path):
        return NotImplemented

    @abstractmethod
    def keychain_is_already_initialised(self):
        return NotImplemented
