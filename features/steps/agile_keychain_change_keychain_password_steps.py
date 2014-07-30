from behave import given, when, then, step
import os
import openpassword
from openpassword.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException, \
    KeychainLockedException

TEMP_KEYCHAIN_PATH = os.path.join('tests', 'fixtures', 'temp.agilekeychain')


@given('I have a keychain initialised with "{password}"')
def step_impl(context, password):
    context.keychain = openpassword.AgileKeychain(TEMP_KEYCHAIN_PATH)
    context.keychain.initialise(password)
    context.remove_path = TEMP_KEYCHAIN_PATH


@given('I unlock it with "{password}"')
def step_impl(context, password):
    context.keychain.unlock(password)


@given('I don\'t unlock it')
def step_impl(context):
    pass


@when('I change the password to "{password}"')
def step_impl(context, password):
    try:
        context.keychain.set_password(password)
    except KeychainLockedException:
        context.exception_was_raised = True


@then('I should be able to unlock it with "{password}"')
def step_impl(context, password):
    context.keychain.unlock(password)


@then('a KeychainLockedException should be raised')
def step_impl(context):
    assert context.exception_was_raised
