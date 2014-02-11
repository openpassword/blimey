from openpassword.exceptions import InvalidMetadataException


class MetaItem(object):
    def __init__(self, data):
        self.data = data

        self.set_title()
        self.set_unique_id()

    def set_title(self):
        self._set_data('title')

    def set_unique_id(self):
        self._set_data('unique_id')

    def _set_data(self, key):
        if key in self.data:
            self.__setattr__(key, self.data[key])
        else:
            raise InvalidMetadataException("{0} not found in provided data.".format(key))
