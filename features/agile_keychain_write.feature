Feature: Add credentials to an agile keychain via API
  So that I can store my passwords
  As an API user
  I must be able to add credentials to the keychain

  Scenario: Adding website credentials to the keychain
    Given I have an initialised keychain
    When I append new data to the keychain
    Then that data should be stored in the agile keychain file structure

  Scenario: Adding credentials without an id attribute fails
    Given I have an initialised keychain
    When I append data missing a usable id
    Then a MissingIdAttributeException should be raised
