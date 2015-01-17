from openpassword import *

keychain = AgileKeychain('test.agilekeychain')
keychain.initialise('password')
keychain.unlock('password')

item = AgileKeychainItem()

keychain._data_source.add_item(item)
