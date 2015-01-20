import os
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import b64encode, b64decode

from openpassword.exceptions import KeyValidationException
from openpassword.agile_keychain._key import EncryptedKey, DecryptedKey


def generate_id():
    return MD5.new(os.urandom(32)).hexdigest().upper()


def decrypt_key(encrypted_key, password):
    password_key_iv = _derive_key_from_password(encrypted_key, password)
    master_key = _aes_decrypt(password_key_iv[0:16], password_key_iv[16:], encrypted_key.data[16:])

    validation_key_iv = _derive_validation_key(encrypted_key, master_key)
    validation_key = _aes_decrypt(validation_key_iv[0:16], validation_key_iv[16:], encrypted_key.validation[16:])

    if master_key != validation_key:
        raise KeyValidationException()

    return DecryptedKey({
        'identifier': encrypted_key.identifier,
        'level': encrypted_key.level,
        'iterations': encrypted_key.iterations,
        'key': master_key
    })


def encrypt_key(decrypted_key, password, iterations=None):
    if iterations is None:
        iterations = decrypted_key.iterations

    master_salt = os.urandom(8)
    master_key = decrypted_key.key

    master_key_iv = PBKDF2(password, master_salt, iterations).read(32)
    encrypted_master_key = _aes_encrypt(master_key_iv[0:16], master_key_iv[16:], master_key)

    validation_salt = os.urandom(8)
    validation_key_iv = _derive_openssl_key(master_key, validation_salt)
    encrypted_validation_key = _aes_encrypt(validation_key_iv[0:16], validation_key_iv[16:], master_key)

    master_key = b'Salted__' + master_salt + encrypted_master_key
    validation_key = b'Salted__' + validation_salt + encrypted_validation_key

    return EncryptedKey({
        'identifier': decrypted_key.identifier,
        'level': decrypted_key.level,
        'iterations': iterations,
        'data': (b64encode(master_key) + b'\x00').decode('ascii'),
        'validation': (b64encode(validation_key) + b'\x00').decode('ascii')
    })


def create_key(password, level, iterations):
    master_salt = os.urandom(8)
    master_key = os.urandom(1024)

    master_key_iv = PBKDF2(password, master_salt, iterations).read(32)
    encrypted_master_key = _aes_encrypt(master_key_iv[0:16], master_key_iv[16:], master_key)

    validation_salt = os.urandom(8)
    validation_key_iv = _derive_openssl_key(master_key, validation_salt)
    encrypted_validation_key = _aes_encrypt(validation_key_iv[0:16], validation_key_iv[16:], master_key)

    master_key = b'Salted__' + master_salt + encrypted_master_key
    validation_key = b'Salted__' + validation_salt + encrypted_validation_key

    return EncryptedKey({
        'identifier': generate_id(),
        'level': level,
        'iterations': iterations,
        'data': (b64encode(master_key) + b'\x00').decode('ascii'),
        'validation': (b64encode(validation_key) + b'\x00').decode('ascii')
    })


def _derive_key_from_password(key, password):
    return PBKDF2(password, key.data[8:16], key.iterations).read(32)


def _derive_validation_key(key, encryption_key):
    return _derive_openssl_key(encryption_key, key.validation[8:16])


def _derive_openssl_key(key, salt):
    key = key[0:-16]
    openssl_key = bytes()
    prev = bytes()
    while len(openssl_key) < 32:
        prev = MD5.new(prev + key + salt).digest()
        openssl_key += prev

    return openssl_key


def _aes_encrypt(key, init_vector, data):
    return AES.new(key, AES.MODE_CBC, init_vector).encrypt(data)


def _aes_decrypt(key, init_vector, data):
    return AES.new(key, AES.MODE_CBC, init_vector).decrypt(data)
