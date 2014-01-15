from nose.tools import *
from openpassword.crypt_utils import *


class CryptUtilsSpec:
    def it_decrypts_a_string_with_the_right_iv_key(self):
        eq_(decrypt(b'\x17\xb1\x08=&N"<u\xe2\x0f&\n#\x1d\xb6', 'this is 16b key!abc123321bca9876'), b'my data is 16b!!')

    def it_fails_to_decrypt_a_string_with_the_wrong_iv_key(self):
        assert decrypt(b'\x17\xb1\x08=&N"<u\xe2\x0f&\n#\x1d\xb6',
                       'this is 15b key!abc123321bca9876') != b'my data is 16b!!'
