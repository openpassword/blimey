from abc import ABCMeta, abstractmethod


class KeychainItemRepository(metaclass=ABCMeta):

    @abstractmethod
    def item_by_unique_id(self, unique_id):
        return NotImplemented

    @abstractmethod
    def filter(self, callback):
        return NotImplemented

    @abstractmethod
    def all_items(self):
        return NotImplemented
