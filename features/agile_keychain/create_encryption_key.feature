Feature: Create encryption key

  Scenario: Initialising a keychain
    Given fixtuers keychain
    Then an encryption key and a validation string should be created
    And the key should be AES CBC decryptable by the key derived from "masterpassword123" using PBKDF2 with "25000" iterations
    And the key should match the validation key decrypted with a key derived from the key itself
