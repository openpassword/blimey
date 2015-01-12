from behave import given, when, then, step
import os
import sys
import openpassword
import plistlib
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import b64decode
from openpassword.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException

TEST_KEYCHAIN_PATH = os.path.join('tests', 'fixtures', 'test.agilekeychain')


@given('fixtuers keychain')
def step_impl(context):
    pass


@then('an encryption key and a validation string should be created')
def step_impl(context):
    data_default_dir = os.path.join(TEST_KEYCHAIN_PATH, "data", "default")
    keys_file = os.path.join(data_default_dir, '1password.keys')
    context.key_object = read_key_object_from_keys_plist_file(keys_file)

    assert context.key_object['data']
    assert context.key_object['validation']


@then('the key should be AES CBC decryptable by the key derived from "{password}" using PBKDF2 with "25000" iterations')
def step_impl(context, password):
    context.encryption_key = decrypt_encryption_key(context.key_object, password)


@then('the key should match the validation key decrypted with a key derived from the key itself')
def step_impl(context):
    context.validation_key = decrypt_validation_key(context.key_object, context.encryption_key)

    assert context.validation_key == context.encryption_key


def read_key_object_from_keys_plist_file(path):
    data = open(path, 'rb').read()
    data = remove_null_bytes(data)

    if sys.version_info < (3, 4, 0):
        keys = plistlib.readPlistFromBytes(data)
    else:
        keys = plistlib.loads(data)

    key = extract_default_key(keys)
    key['data'] = b64decode(key['data'])
    key['validation'] = b64decode(key['validation'])

    return key


def remove_null_bytes(data):
    result = b''
    last = 0

    index = data.find(b'\x00')
    while index != -1:
        result = result + data[last:index]
        last = index + 1
        index = data.find(b'\x00', last)

    result = result + data[last:]

    return result


def extract_default_key(keys):
    for key in keys['list']:
        if key['level'] == 'SL5':
            return key


def decrypt_encryption_key(key_object, password):
    password_key = derive_key_from_password(key_object, password)
    return decrypt(key_object['data'][16:], password_key)


def derive_key_from_password(key_object, password):
    key = PBKDF2(password, key_object['data'][8:16], key_object['iterations'])
    return key.read(32)


def decrypt(data, key_iv):
    key = key_iv[0:16]
    iv = key_iv[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return cipher.decrypt(data)


def decrypt_validation_key(key_object, encryption_key):
    validation_key = derive_validation_key(key_object, encryption_key)
    return decrypt(key_object['validation'][16:], validation_key)


def derive_validation_key(key_object, encryption_key):
    return derive_openssl_key(encryption_key, key_object['validation'][8:16])


def derive_openssl_key(key, salt):
    key = key[0:-16]
    openssl_key = bytes()
    prev = bytes()
    while len(openssl_key) < 32:
        prev = MD5.new(prev + key + salt).digest()
        openssl_key += prev

    return openssl_key
