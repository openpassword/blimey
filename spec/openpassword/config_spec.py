from nose.tools import assert_equals
from openpassword.config import Config

class ConfigSpec:

    def it_sets_the_path_to_the_keychain(self):
        cfg = Config()
        cfg.set_path("path/to/keychain")
        assert_equals(cfg.get_path(), "path/to/keychain")

