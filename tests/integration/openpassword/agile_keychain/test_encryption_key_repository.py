import os
from nose.tools import *
from openpassword.agile_keychain import EncryptionKeyRepository
from openpassword.exceptions import EncryptionKeyNotFoundException
from openpassword.exceptions import InvalidPathException


class EncryptionKeyRepositoryTest:
    def setUp(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        fixture_path = current_path + '/../../../fixtures/test.agilekeychain'

        self.repository = EncryptionKeyRepository(fixture_path)

    def it_returns_encryption_key_for_given_security_level(self):
        key = self.repository.key_for_security_level("SL5")

        eq_(key.get_id(), "98EB2E946008403280A3A8D9261018A4")

    @raises(EncryptionKeyNotFoundException)
    def it_raises_invalidsecuritylevelexception_if_no_key_found(self):
        self.repository.key_for_security_level("SL4")

    @raises(InvalidPathException)
    def it_raises_invaliduuidexception_when_uuid_is_not_valid(self):
        self.repository = EncryptionKeyRepository('invalid/keychain/path')
        self.repository.key_for_security_level("SL5")
