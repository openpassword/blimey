Feature:
  In order to have a secure keychain
  As an API user
  I want to be able to lock and unlock a keychain
  So I can make sure secret data is available only when authorised

Scenario: Unlocking a keychain
  Given I have a locked keychain
  When I unlock it
  Then it will become unlocked
  And I will be able to see it's contents

Scenario: Locking a keychain
  Given I have an unlocked keychain
  When I lock the keychain
  Then it will become locked
