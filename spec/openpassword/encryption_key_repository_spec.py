import os
from nose.tools import *
from openpassword import EncryptionKeyRepository


class EncryptionKeyRepositorySpec:
    def setUp(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        fixture_path = current_path + '/../fixtures/test.agilekeychain'

        self.repository = EncryptionKeyRepository(fixture_path)

    def it_returns_encryption_key_for_given_security_level(self):
        sl3 = self.repository.key_for_security_level("SL3")
        sl5 = self.repository.key_for_security_level("SL5")

        eq_(sl3["identifier"], "BE4CC37CD7C044E79B5CC1CC19A82A13")
        eq_(sl5["identifier"], "98EB2E946008403280A3A8D9261018A4")
