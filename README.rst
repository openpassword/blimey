blimey
======

A Python library for interacting with 1Password's AgileKeychain password storage. Supports keychains created with 1Password 3 through 5.

Features

* Unlocking/locking the keychain
* Iterating over the keychain contents
* Creating new keychain items
* Editing keychain items

Planned

* Removing keychain items with support for the trash functionality
* Support for other password managers

Development status
------------------

Stable (master)

.. image:: https://secure.travis-ci.org/openpassword/blimey.png?branch=master
  :alt: Build status

.. image:: https://scrutinizer-ci.com/g/openpassword/blimey/badges/quality-score.png?b=master
  :alt: Quality

.. image:: https://scrutinizer-ci.com/g/openpassword/blimey/badges/coverage.png?b=master
  :alt: Coverage


Unstable (develop)

.. image:: https://secure.travis-ci.org/openpassword/blimey.png?branch=develop
  :alt: Build status

.. image:: https://scrutinizer-ci.com/g/openpassword/blimey/badges/quality-score.png?b=develop
  :alt: Quality

.. image:: https://scrutinizer-ci.com/g/openpassword/blimey/badges/coverage.png?b=develop
  :alt: Coverage

License
-------

.. image:: http://b.repl.ca/v1/License-MIT-blue.png
  :alt: MIT License

Usage
-----

.. code-block:: python

    from blimey import AgileKeychain

    # Construct a keychain with either a path to an existing keychain,
    # or the path to where you want your keychain created
    agilekeychain = AgileKeychain('path/to/keychain.agilekeychain')

    # If the keychain doesn't exist, initialise it with a master password
    agilekeychain.initialise('super-secret-password')

    # Existing (and newly crated) keychains are unlocked by calling the unlock method
    agilekeychain.unlock('super-secret-password')

    # You can change the master password by calling set_password
    agilekeychain.set_password('even-more-secret-password')

    # Call create_item to initialise a new item
    item = agilekeychain.create_item()

    # Some boilerplate is put in place automatically
    print(item)
    # AgileKeychainItem({'encrypted': {}, 'title': 'Untitled', 'createdAt': 1422404797.4550807,
    # 'typeName': 'passwords.Password', 'keyID': 'ED7D542C2EA24479407D3D5CB35637D2', 'location': '',
    # 'uuid': 'CBA45A598A4A63D4DDD3C78E2CC11666', 'locationKey': ''})

    # The item behaves like any dictionary
    item['title'] = 'Usage Example'

    # Anything stored under 'encrypted' key will be encrypted on save
    item['encrypted'] = {
        'username': 'patrick',
        'password': 'correct horse battery staple'
    }

    # To save an item, pass it to the save_item method
    agilekeychain.save_item(item)

    # To access keychain items, you can iterate over the keychain, ...
    for item in agilekeychain:
        print(item['title'])
    # AgileKeychainItem({'encrypted': {}, 'title': 'Untitled', 'createdAt': 1422404797.4550807,
    # 'typeName': 'passwords.Password', 'keyID': 'ED7D542C2EA24479407D3D5CB35637D2', 'updatedAt': 1422404900,
    # 'location': '', 'uuid': 'CBA45A598A4A63D4DDD3C78E2CC11666', 'locationKey': ''})

    # ... or access them directly by their UUID
    print(agilekeychain['905B51856FD59A3C3AEF42A9FCE47E87'])

    # When you are done you can lock the keychain by calling the lock method
    agilekeychain.lock()

