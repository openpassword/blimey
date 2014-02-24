OpenPassword
============
![License MIT](http://b.repl.ca/v1/License-MIT-blue.png)

Master Build Status
-------------------
[![Build Status](https://secure.travis-ci.org/OpenPassword/OpenPasswordLib.png?branch=master)](http://travis-ci.org/OpenPassword/OpenPasswordLib)

Develop Build Status
--------------------
[![Build Status](https://secure.travis-ci.org/OpenPassword/OpenPasswordLib.png?branch=develop)](http://travis-ci.org/OpenPassword/OpenPasswordLib)

Usage
=====

```python
import openpassword

keychain = openpassword.AgileKeychain(path_to_agile_keychain)
keychain.unlock("masterpassword123")

items = keychain.search("Folder")
item = keychain.get_item_by_unique_id(items[0].uuid)
```

Note that "items[0]" and "item" will be the same keychain item, but keychain.get_item_by_unique_id method will return an already decrypted item, while the items returned by keychain.search are still encrypted and still need you to call decrypt on them.
