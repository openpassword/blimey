from Crypto.Cipher import AES


def decrypt(data, key_iv):
    key = key_iv[0:16]
    iv = key_iv[16:]
    print(data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(data)


def encrypt(data, key_iv):
    key = key_iv[0:16]
    iv = key_iv[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(data)
