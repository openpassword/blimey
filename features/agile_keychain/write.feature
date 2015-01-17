Feature: Add an item to an agile keychain via API
  So that I can store my secrets
  As an API user
  I must be able to add items to the keychain

#  Scenario: Adding a password to the keychain
#    Given I have an initialised keychain
#    When I append a new password to the keychain
#    Then that password should be stored in the agile keychain file structure

  Scenario: Adding an item without an id attribute fails
    Given I have an initialised keychain
    When I append an item missing a usable id
    Then a MissingIdAttributeException should be raised
