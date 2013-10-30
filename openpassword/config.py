import traceback

class Config:
    def __init__(self):
        self._path = None

    def set_path(self, path = None):
        self._path = path

    def get_path(self):
        return self._path
