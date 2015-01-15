Feature: Change keychain password
  So that I can keep my keychain secured
  As an API user
  I want to be able to change the keychain password

#  Scenario: Changing keychain password
#    Given I have a keychain initialised with "oldpassword"
#    And I unlock it with "oldpassword"
#    When I change the password to "newpassword"
#    Then I should be able to unlock it with "newpassword"

  Scenario: Attempting to change password of a locked keychain
    Given I have a keychain initialised with "oldpassword"
    And I don't unlock it
    When I change the password to "newpassword"
    Then a KeychainLockedException should be raised
