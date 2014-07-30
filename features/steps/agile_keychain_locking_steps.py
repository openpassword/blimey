from behave import given, when, then, step
import os
import openpassword
from openpassword.exceptions import IncorrectPasswordException

TEMP_KEYCHAIN_PATH = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
CORRECT_PASSWORD = "correctpassword"
INCORRECT_PASSWORD = "incorrectpassword"


@given('I have a locked keychain')
def step_impl(context):
    _add_new_keychain_to_context(context)


@given('I have an unlocked keychain')
def step_impl(context):
    _add_new_keychain_to_context(context)
    context.keychain.unlock(CORRECT_PASSWORD)


@when('I unlock it')
def step_impl(context):
    context.keychain.unlock(CORRECT_PASSWORD)


@when('I lock it')
def step_impl(context):
    context.keychain.lock()


@when('I try to unlock it with an incorrect password')
def step_impl(context):
    try:
        context.keychain.unlock(INCORRECT_PASSWORD)
    except IncorrectPasswordException:
        context.exception_was_raised = True


@then('it will become locked')
def step_impl(context):
    assert context.keychain.is_locked() is True


@then('it will become unlocked')
def step_impl(context):
    assert context.keychain.is_locked() is False


@then('I will be able to see its contents')
def step_impl(context):
    try:
        items = list(context.keychain)
    except TypeError:
        assert False


@then('an IncorrectPasswordException should be raised')
def step_impl(context):
    if not context.exception_was_raised:
        assert False


def _add_new_keychain_to_context(context):
    context.keychain = openpassword.AgileKeychain(TEMP_KEYCHAIN_PATH)
    context.keychain.initialise(CORRECT_PASSWORD)
    context.remove_path = TEMP_KEYCHAIN_PATH
