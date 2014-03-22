Feature: Initialise keychain
  So that I can have a keychain to store my passwords
  As an API user
  I must be able to initialise a new keychain

  Scenario: Attempting to unlock a non-initialised keychain
    Given I have an non-initialised keychain
    When I try to unlock it
    Then I should get a NonInitialisedKeychainException

  Scenario: Initialising a keychain
    Given I have a non-initialised keychain in "keychainpath"
    When I initialise it using "mypassword"
    Then the agile keychain folder structure is created

  Scenario: Already Initialised keychain
    Given I have a keychain that is already initialised
    When I check it initialisation status
    Then It should be reported as initialised

  Scenario: Attempting to initialise an already initialised keychain
    Given I have an initialised keychain
    When I try to initialise it
    Then I should get a KeychainAlreadyInitialisedException