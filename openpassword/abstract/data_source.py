from abc import ABCMeta, abstractmethod


class DataSource(metaclass=ABCMeta):
    @abstractmethod
    def initialise(self, path, config=None):
        return NotImplemented

    @abstractmethod
    def is_initialised(self):
        return NotImplemented

    @abstractmethod
    def authenticate(self, password):
        return NotImplemented

    @abstractmethod
    def deauthenticate(self):
        return NotImplemented

    @abstractmethod
    def is_authenticated(self):
        return NotImplemented

    @abstractmethod
    def set_password(self, password):
        return NotImplemented

    @abstractmethod
    def save_item(self, item):
        return NotImplemented

    @abstractmethod
    def get_item_by_id(self, item):
        return NotImplemented

    @abstractmethod
    def get_all_items(self):
        return NotImplemented
