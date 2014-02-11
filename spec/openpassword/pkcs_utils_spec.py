from nose.tools import *
from openpassword.pkcs_utils import *


class PkscUtilsSpec:
    def it_leaves_bytes_of_correct_length_unpadded(self):
        eq_(strip_byte_padding(b"12345678"), b"12345678")

    def it_strips_byte_padding(self):
        eq_(strip_byte_padding(b"12345678abc\x05\x05\x05\x05\x05"), b"12345678abc")
        eq_(strip_byte_padding(b"12345678abcdefgh"), b"12345678abcdefgh")

    @raises(ValueError)
    def it_raises_value_error_if_padded_byte_input_length_not_multiple_of_padding_length(self):
        strip_byte_padding(b"12345678abc\x05\x05\x05\x05")

    def it_pads_input_bytes_to_padding_length(self):
        eq_(byte_pad(b'{"foo": "bar"}', 16), b'{"foo": "bar"}\x02\x02')

    @raises(ValueError)
    def it_raises_value_error_if_padding_to_greater_than_256_bytes(self):
        byte_pad(b"foobar", 257)
