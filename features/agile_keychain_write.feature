Feature: API user adds credentials to an agile keychain
  So that I can store my passwords
  As an API user
  I must be able to add credentials to the keychain

  Scenario: Adding website credentials to the keychain
    Given I have an initialised keychain
    When I append new data to the keychain
    Then that data should be stored in the agile keychain file structure