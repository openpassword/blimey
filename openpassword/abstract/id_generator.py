from abc import ABCMeta, abstractmethod

class IdGenerator(metaclass=ABCMeta):
    @abstractmethod
    def generate_id(self):
        return NotImplemented
