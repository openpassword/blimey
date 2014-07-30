Feature: Lock and Unlock a keychain
  So that I can control access to my keychain
  As an API user
  I want to be able to lock and unlock my keychain at will

Scenario: Unlocking a keychain
  Given I have a locked keychain
  When I unlock it
  Then it should become unlocked
  And I should be able to see its contents

Scenario: Failing to unlock a keychain
  Given I have a locked keychain
  When I try to unlock it with an incorrect password
  Then an IncorrectPasswordException should be raised

Scenario: Locking a keychain
  Given I have an unlocked keychain
  When I lock it
  Then it should become locked
