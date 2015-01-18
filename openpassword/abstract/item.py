from abc import ABCMeta, abstractmethod


class Item(metaclass=ABCMeta):
    @abstractmethod
    def get_id(self):
        return NotImplemented
