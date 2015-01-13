import os
import json
import plistlib
from base64 import b64encode
from pbkdf2 import PBKDF2
from openpassword import abstract
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from string import Template

AGILE_KEYCHAIN_BASE_FILES = ['1password.keys', 'contents.js', 'encryptionKeys.js']


class DataSource(abstract.DataSource):
    def __init__(self, path):
        self.base_path = path
        self._default_folder = os.path.join(self.base_path, "data", "default")

    def initialise(self, password):
        os.makedirs(self._default_folder)

        for agile_keychain_base_file in AGILE_KEYCHAIN_BASE_FILES:
            open(os.path.join(self._default_folder, agile_keychain_base_file), "w+").close()

        self._initialise_key_files(password)

        self.set_password(password)

    def is_keychain_initialised(self):
        return self._validate_agile_keychain_base_files() and self._is_valid_folder(self._default_folder)

    def add_item(self, item):
        file_handle = open(os.path.join(self._default_folder, "{0}.1password".format(item['id'])), "w")
        json.dump(item, file_handle)
        file_handle.close()

    def verify_password(self, password):
        file_handle = open(os.path.join(self._default_folder, "encryptionKeys.js"), "r")
        password_found = False

        if password in file_handle.read():
            password_found = True

        file_handle.close()
        return password_found

    def set_password(self, password):
        file_handle = open(os.path.join(self._default_folder, "encryptionKeys.js"), "w")
        file_handle.write(password)
        file_handle.close()

    def _validate_agile_keychain_base_files(self):
        is_initialised = True
        for base_file in AGILE_KEYCHAIN_BASE_FILES:
            current_file = os.path.join(self._default_folder, base_file)
            is_initialised = is_initialised and self._is_valid_file(current_file)
        return is_initialised

    def _is_valid_file(self, file):
        return os.path.exists(file) and os.path.isfile(file)

    def _is_valid_folder(self, folder):
        return os.path.exists(folder) and os.path.isdir(folder)

    def _initialise_key_files(self, password):
        salt = os.urandom(8)
        master_key = os.urandom(1024)

        pbkdf = PBKDF2(password, salt, 25000)
        key = pbkdf.read(16)
        iv = pbkdf.read(16)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_master_key = cipher.encrypt(master_key)

        validation_salt = os.urandom(8)
        validation_key_iv = self._derive_openssl_key(master_key, validation_salt)

        cipher = AES.new(validation_key_iv[0:16], AES.MODE_CBC, validation_key_iv[16:])
        encrypted_validation_key = cipher.encrypt(master_key)

        data = b64encode(b'Salted__' + salt + encrypted_master_key) + b'\x00'
        validation = b64encode(b'Salted__' + validation_salt + encrypted_validation_key) + b'\x00'

        keys = {
            'SL3': '123',
            'SL5': '456',
            'list': [
                {
                    'identifier': '123',
                    'iterations': 25000,
                    'data': data.decode('ascii'),
                    'validation': validation.decode('ascii'),
                    'level': 'SL3'
                },
                {
                    'identifier': '456',
                    'iterations': 25000,
                    'data': data.decode('ascii'),
                    'validation': validation.decode('ascii'),
                    'level': 'SL5'
                }
            ]
        }

        plist_template = Template("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>SL3</key>
    <string>$identifier3</string>
    <key>SL5</key>
    <string>$identifier5</string>
    <key>list</key>
    <array>
        <dict>
            <key>data</key>
            <string>$data3</string>
            <key>identifier</key>
            <string>$identifier3</string>
            <key>iterations</key>
            <integer>$iterations3</integer>
            <key>level</key>
            <string>SL3</string>
            <key>validation</key>
            <string>$validation3</string>
        </dict>
        <dict>
            <key>data</key>
            <string>$data5</string>
            <key>identifier</key>
            <string>$identifier5</string>
            <key>iterations</key>
            <integer>$iterations5</integer>
            <key>level</key>
            <string>SL5</string>
            <key>validation</key>
            <string>$validation5</string>
        </dict>
    </array>
</dict>
</plist>
""")

        subs = {
            'identifier3': keys['list'][0]['identifier'],
            'data3': keys['list'][0]['data'],
            'iterations3': keys['list'][0]['iterations'],
            'validation3': keys['list'][0]['validation'],
            'identifier5': keys['list'][1]['identifier'],
            'data5': keys['list'][1]['data'],
            'iterations5': keys['list'][1]['iterations'],
            'validation5': keys['list'][1]['validation']
        }

        file_handle = open(os.path.join(self._default_folder, "1password.keys"), "w")
        file_handle.write(plist_template.substitute(subs))
        file_handle.close()

    def _derive_openssl_key(self, key, salt):
        key = key[0:-16]
        openssl_key = bytes()
        prev = bytes()
        while len(openssl_key) < 32:
            prev = MD5.new(prev + key + salt).digest()
            openssl_key += prev

        return openssl_key
