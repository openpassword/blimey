Feature: Initialise a keychain
  So that I can have a keychain to store my passwords
  As an API user
  I must be able to initialise a new keychain

  Scenario: Attempting to unlock a non-initialised keychain
    Given I have a non-initialised keychain
    When I try to unlock it
    Then a NonInitialisedKeychainException should be raised

  Scenario: Initialising a keychain
    Given I have a non-initialised keychain
    When I initialise it using "mypassword"
    Then the agile keychain folder structure should be created
    And I should be able to unlock the agile keychain with "mypassword"

  Scenario: Checking status of an initialised keychain
    Given I have an initialised keychain
    When I check its initialisation status
    Then it should be initialised

  Scenario: Checking status of a non initialised keychain
    Given I have a non-initialised keychain
    When I check its initialisation status
    Then it should not be initialised

  Scenario: Attempting to initialise an already initialised keychain
    Given I have an initialised keychain
    When I try to initialise it
    Then a KeychainAlreadyInitialisedException should be raised