Feature: Retrieving items from the keychain
  So that I can retrieve my secrets
  As an API user
  I must be able to get items from the keychain

  Scenario: Retrieving an item from the keychain
    Given I have an initialised keychain
    And an item with ID "123" has been added to the keychain
    When I get an item by ID "123"
    Then I should get the added item

  Scenario: Retrieving all items from the keychain
    Given I have an initialised keychain
    And a number of items is added to the keychain
    When I iterate the items in the keychain
    Then I should encounter all the added items
