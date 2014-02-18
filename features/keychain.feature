Feature: Manipulating a keychain

Scenario: Unlocking a keychain
  Given I have a locked keychain
  When I unlock it
  Then it will become unlocked

Scenario: Getting item by unique id
  Given I have an unlocked keychain
  And  the keychain has an item with id "9E7673CCBB5B4AC9A7A8838835CB7E83"
  When I request item with the given id
  Then I should get the item with that id

  Scenario: Getting all items of a keychain
    Given I have an unlocked keychain
    And the keychain has a given number of items
    When I request all items from the keychain
    Then I should get a collection with the right number of items

  Scenario: Locking a keychain
    Given I have an unlocked keychain
    When I lock the keychain
    Then it will become locked
