from Crypto.Hash import MD5


def derive_openssl_key(key, salt, hash=MD5):
    key = key[0:-16]
    openssl_key = bytes()
    prev = bytes()
    while len(openssl_key) < 32:
        prev = hash.new(prev + key + salt).digest()
        openssl_key += prev

    return openssl_key
