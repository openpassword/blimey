from openpassword.exceptions import InvalidPasswordException
from multiprocessing import Pool

import time


def lock_countdown(timeout):
    time.sleep(timeout)


class Keychain:

    def __init__(self, encryption_key, timeout=60, lock_callback=None):
        self.encryption_key = encryption_key
        self._locked = True
        self._timeout = timeout
        self._pool = Pool(1)
        self._lock_callback = lock_callback

    def unlock(self, password):
        try:
            self.encryption_key.decrypt(password)
            self._locked = False
            self._start_lock_countdown()
        except InvalidPasswordException as e:
            self._locked = True
            raise(e)

    def _start_lock_countdown(self):
        self._pool.apply_async(lock_countdown, (self._timeout, ), callback=self._on_lock_timeout)

    def _on_lock_timeout(self, parameter):
        self._locked = True
        if callable(self._lock_callback):
            self._lock_callback()

    def is_locked(self):
        return self._locked
