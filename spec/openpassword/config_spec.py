from nose.tools import *
from openpassword import Config

class ConfigSpec:

    def it_sets_the_path_to_the_keychain(self):
        cfg = Config()
        cfg.set_path("path/to/keychain")
        eq_(cfg.get_path(), "path/to/keychain")

