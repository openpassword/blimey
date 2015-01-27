from behave import given, when, then, step
import os
import blimey
from blimey.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException

TEMP_KEYCHAIN_PATH = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
CORRECT_PASSWORD = "correctpassword"
INCORRECT_PASSWORD = "incorrectpassword"


@given('I have a non-initialised keychain')
def step_impl(context):
    context.keychain = blimey.AgileKeychain(TEMP_KEYCHAIN_PATH)


@given('I have an initialised keychain')
def step_impl(context):
    context.keychain = blimey.AgileKeychain(TEMP_KEYCHAIN_PATH)
    context.keychain.initialise(CORRECT_PASSWORD, {'iterations': 10})
    context.remove_path = TEMP_KEYCHAIN_PATH


@when('I try to unlock it')
def step_impl(context):
    context.lock_failed = False
    try:
        context.keychain.unlock("somepassword")
    except NonInitialisedKeychainException:
        context.lock_failed = True


@when('I initialise it using "{password}"')
def step_impl(context, password):
    context.keychain.initialise(password, {'iterations': 10})
    context.remove_path = TEMP_KEYCHAIN_PATH


@when('I check its initialisation status')
def step_impl(context):
    context.keychain_initialisations_state = context.keychain.is_initialised()


@when('I try to initialise it')
def step_impl(context):
    context.initialisation_failed = False
    try:
        context.keychain.initialise("somepassword", {'iterations': 10})
    except KeychainAlreadyInitialisedException:
        context.initialisation_failed = True


@then('a NonInitialisedKeychainException should be raised')
def step_impl(context):
    assert context.lock_failed is True


@then('the agile keychain folder structure should be created')
def step_impl(context):
        assert os.path.exists(TEMP_KEYCHAIN_PATH) and os.path.isdir(TEMP_KEYCHAIN_PATH)

        data_default_dir = os.path.join(TEMP_KEYCHAIN_PATH, "data", "default")
        assert os.path.exists(data_default_dir) and os.path.isdir(data_default_dir)

        keys_file = os.path.join(data_default_dir, '1password.keys')
        assert os.path.exists(keys_file) and os.path.isfile(keys_file)

        contents_file = os.path.join(data_default_dir, 'contents.js')
        assert os.path.exists(contents_file) and os.path.isfile(contents_file)

        encryption_keys_file = os.path.join(data_default_dir, 'encryptionKeys.js')
        assert os.path.exists(encryption_keys_file) and os.path.isfile(encryption_keys_file)


@then('I should be able to unlock the agile keychain with "{password}"')
def step_impl(context, password):
    context.keychain.unlock(password)


@then('it should be initialised')
def step_impl(context):
    assert context.keychain_initialisations_state is True


@then('it should not be initialised')
def step_impl(context):
    assert context.keychain.is_initialised() is False


@then('a KeychainAlreadyInitialisedException should be raised')
def step_impl(context):
    assert context.initialisation_failed is True
