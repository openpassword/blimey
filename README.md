OpenPassword
============

Master Build Status
-------------------
[![Build Status](https://secure.travis-ci.org/OpenPassword/OpenPassword.png?branch=master)](http://travis-ci.org/OpenPassword/OpenPassword)

Develop Build Status
--------------------
[![Build Status](https://secure.travis-ci.org/OpenPassword/OpenPassword.png?branch=develop)](http://travis-ci.org/OpenPassword/OpenPassword)

Usage
=====

```python
import openpassword

keychain = openpassword.AgileKeychain(path_to_agile_keychain)
keychain.unlock("masterpassword123")
item = self.keychain.get_item_by_unique_id("9E7673CCBB5B4AC9A7A8838835CB7E83")
```
