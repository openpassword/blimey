import os
from nose.tools import *
from openpassword import EncryptionKeyRepository


class EncryptionKeyRepositoryTest:
    def setUp(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        fixture_path = current_path + '/../fixtures/test.agilekeychain'

        self.repository = EncryptionKeyRepository(fixture_path)

    def it_returns_encryption_key_for_given_security_level(self):
        key = self.repository.key_for_security_level("SL5")

        eq_(key.get_id(), "98EB2E946008403280A3A8D9261018A4")
