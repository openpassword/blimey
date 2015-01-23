from nose.tools import raises

from openpassword.agile_keychain.agile_keychain_item import EncryptedAgileKeychainItem, AgileKeychainItem


class AgileKeychainItemSpec:
    def it_represents_itself_as_agile_keychain_item(self):
        item = AgileKeychainItem({'foo': 'bar'})

        assert repr(item) == "AgileKeychainItem({'foo': 'bar'})"


class EncryptedAgileKeychainItemSpec:
    def it_represents_itself_as_encrypted_agile_keychain_item(self):
        item = EncryptedAgileKeychainItem({'foo': 'bar'})

        assert repr(item) == "EncryptedAgileKeychainItem({'foo': 'bar'})"
