from nose.tools import *
from openpassword.agile_keychain.keychain_item import KeychainItem
from base64 import b64decode


class KeychainItemSpec:
    def setUp(self):
        self.item = {
            "createdAt": 1383517732,
            "locationKey": "someotherwebsite.com",
            "updatedAt": 1383517785,
            "keyID": "98EB2E946008403280A3A8D9261018A4",
            "openContents": {
                "contentsHash": "476e4c70",
                "tags": [
                    "tag2"
                ],
                "usernameHash": "451fb2b0e27676633a9677dbfa5f6f23f4d21fbbadc6af0b20a676770c7f9b47"
            },
            "uuid": "97019BEBCF9E402F8F0C033474B1B85D",
            "encrypted": "U2FsdGVkX19TftTVzivSyCJAgFfjwPRvhLzOGUCim+SAat+JZBeOdP86oh7B/rfV/k08DmJn2+ZwgQuss8KJMCb+P/mu+sISK7LRpXgCZJ1dx0D+DWQOZB+gXJXtlz9TmKNNOVBswYHl0qhfaGpFAQgwnPEcDoubmxK2sh2AU88hnmJNND054M0i4QXjdO4xsyalzK09fEDlaoRRjd+TlbKVoycBIwWDihbUloMezTs=\u0000",  # nopep8
            "typeName": "webforms.WebForm",
            "location": "http://www.someotherwebsite.com",
            "title": "Some Other Website"
        }

        self.keychain_item = KeychainItem(self.item)
        self.decryption_key = b64decode("vvvspiWrNzItmGcelM+MM8w28CQCNQYGtVCB5GbihDktjUETw7/mEfg+nnEo3DthKXisz3R+NhvQbvqoF+yBHK/Z4LvQvEx8x5KagvxLvcojYmYhtfS6bDmiUqLC+Mdc3KQo9AffqGOmbklcvfzy+Yyczt4Wy6MXDXZT2lan6tzY+RlL5gOvbqcWPq8gv9Yw2I2enhiv5R4MNzlb/4nf4TsMVqV50dzzc0L9NNfunhweoaxZ3z0G9gRn0qPsK0P5IzfGCPvycqgL1gqwUqVW1kTHJcEKWp1OE/xnwBwA3mNJmPWBYlOEX+8W6UT5RcHfdkM2rUe3ublPQ1UaLWNMwQoLlLWzqSOEdX4sf9rFeZ5UOjDtvapFkFV8U7Z8cSnZyDdKlQ9lGT2/Qv3rLavuxc6yAw0l9jEaCy11KNgAKKy2Wyc6ubCGw1CEfH72CUKOTlx7yrtuGsaytxtlWI3AitU5tLYXU+S3RyJYKKOYrMTW7joww4j5BKtBg66SNXWzkQRksnrqMCxgOZBYrxLvbBf6dO8UtmtzxNoNOYcRe9doA/hAlIvVsUjDSvtMdzcJ+A56Rb+tpGZClHRuLCBkao9b7OHaW2JjxJaNibE3mONk/UDo6xq6HiOoVqDC2USvgqE/X1XiOy1yU1qUV5wVtbV5+OYf8ubqpRlSOuSytK8lAWxCq8oTOIIPcDR77rkqj6Ou4dMfMyCWIcQ7wtwEdVCU2GzUgro3JdArmXfXwUbRmoX+c/qas6LM5MQs3fTuMooCch6qvikyHA1FrCCPC3wBrwEeyqXPQcmyGeihYWvtmyWmdJcY5c2BsxRDGVfiofcCL6t9ytH3KN33qiOkrllbLauTSNPjf1bRWqZ8G0mBp6hLMk+cg+v1Mw6LQj3wP0+vY1+bZt0MCECRIDhHfh9zS+k6F+K4eOjIO0ZkTEKNeY/rkyQSQNSpA9aOJgY0tQM0PwQMhM9PpEn5oWu2Z9e6G+AkFQg6vHM/d0I5XHVrrVNZlPHK2gPUQ8q9ZsjmbiS6oR8K7IXOfMd5K5UZXizpX3YUr5Et8NTzBy4vExFkEuLFYxyCOzwZYfU3bk3HGEMJYByK3zJWsa84r8QUWk4flU3omQSfA5Mdc/caw74atm/VfP8yMLpuFTiP6wPz4gDhq67r46dNgDDCKDMWCAsigXI1mIPJzDG79/d0w0GyO7oLLnGoptsrYLQxHbfZ+IgzJyGQ2iFxwnLjQKsnJ9vG+7A1w8jyAZij0cRV7hjDs/KaJNXxenCzE0Ofkf6IuMMtIVjbYfD0s8GXIuIAltierebQiA6I1yQtyR8WYfBziSPVTpvYf9SdxzsShlcGihSK33O03enbc6UmAWWtlRAQEBAQEBAQEBAQEBAQEBA=")  # nopep8
        self.test_data = {
            "fields": [
                {
                    "name": "Username",
                    "value": "somedifferentusername",
                    "designation": "username"
                },
                {
                    "name": "Password",
                    "value": "password123",
                    "designation": "password"
                }
            ]
        }

    def it_decrypts_data_with_decryption_key(self):
        self.keychain_item.decrypt(self.decryption_key)

        eq_(self.keychain_item.data, self.test_data)

    def it_invalidates_encrypted_data_when_data_is_set(self):
        self.keychain_item.decrypt(self.decryption_key)
        self.keychain_item.set_private_contents({
            "foo": "bar"
        })

        eq_(self.keychain_item.encrypted, None)

    def it_encrypts_data_with_encryption_key(self):
        test_data = {
            "foo": "bar"
        }

        self.keychain_item.set_private_contents(test_data)
        self.keychain_item.encrypt(self.decryption_key)
        self.keychain_item.decrypt(self.decryption_key)

        eq_(self.keychain_item.data, test_data)

    def it_searches_meta_properties_for_matching_string(self):
        eq_(self.keychain_item.search("website.com"), True)
        eq_(self.keychain_item.search("Some Other"), True)
        eq_(self.keychain_item.search("foobar"), False)
