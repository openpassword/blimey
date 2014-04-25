from nose.tools import *

from openpassword.agile_keychain.id_generator import IdGenerator


class IdGeneratorSpec:
    def it_generates_a_32_bytes_long_string(self):
        id_generator = IdGenerator()
        new_id = id_generator.generate_id()
        eq_(len(new_id), 32)